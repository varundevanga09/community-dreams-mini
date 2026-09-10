import os
import re
import chromadb
from sentence_transformers import SentenceTransformer
from sentence_transformers import CrossEncoder
from groq import Groq

model = SentenceTransformer("all-MiniLM-L6-v2")
reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")
client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_or_create_collection("knowledge_base")
groq_client = Groq(api_key=os.environ["GROQ_API_KEY"])


def clean_answer(text):
    return re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL).strip()


def rerank(question, docs, top_n=3):
    pairs = [[question, doc] for doc in docs]
    scores = reranker.predict(pairs)
    scored_docs = sorted(zip(docs, scores), key=lambda x: x[1], reverse=True)
    return [doc for doc, score in scored_docs[:top_n]], scored_docs


def ask(question, retrieve_k=8, final_k=3):
    q_embedding = model.encode(question).tolist()
    results = collection.query(query_embeddings=[q_embedding], n_results=retrieve_k)
    candidates = results["documents"][0]

    reranked_docs, scored = rerank(question, candidates, top_n=final_k)

    print("\n--- Re-rank scores (all candidates, sorted) ---")
    for doc, score in scored:
        print(f"{score:.3f} | {doc[:60]}...")

    context = "\n\n".join(reranked_docs)

    prompt = f"""You are a community information assistant relaying general educational guidance that has already been reviewed. This is not a diagnosis and you are not creating new medical advice — you are only summarizing the pre-approved reference material below.

Answer the question using ONLY the information in the reference material. If the material doesn't cover it, say "I don't have enough information."

Reference material:
{context}

Question: {question}

Answer:"""

    response = groq_client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=300
    )

    print("\n--- Answer ---")
    print(clean_answer(response.choices[0].message.content))


if __name__ == "__main__":
    while True:
        q = input("\nAsk a question (or 'quit'): ")
        if q.lower() == "quit":
            break
        ask(q)