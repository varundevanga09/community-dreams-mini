import os
import chromadb
from sentence_transformers import SentenceTransformer
from groq import Groq
from sentence_transformers import CrossEncoder

reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")

model = SentenceTransformer("all-MiniLM-L6-v2")
client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_or_create_collection("knowledge_base")
groq_client = Groq(api_key=os.environ["GROQ_API_KEY"])

def ask(question, retrieve_k=8, final_k=3):
    q_embedding = model.encode(question).tolist()
    results = collection.query(query_embeddings=[q_embedding], n_results=retrieve_k)
    candidates = results["documents"][0]

    reranked_docs, scored = rerank(question, candidates, top_n=final_k)

    print("\n--- Re-rank scores (all candidates, sorted) ---")
    for doc, score in scored:
        print(f"{score:.3f} | {doc[:60]}...")

    context = "\n\n".join(reranked_docs)
    prompt = f"""Answer the question using ONLY the context below. If the context doesn't contain the answer, say "I don't have enough information."

Context:
{context}

Question: {question}

Answer:"""

    response = groq_client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[{"role": "user", "content": prompt}]
    )
    print("\n--- Answer ---")
    print(response.choices[0].message.content)

def rerank(question, docs, top_n=3):
    pairs = [[question, doc] for doc in docs]
    scores = reranker.predict(pairs)
    scored_docs = sorted(zip(docs, scores), key=lambda x: x[1], reverse=True)
    return [doc for doc, score in scored_docs[:top_n]], scored_docs

if __name__ == "__main__":
    while True:
        q = input("\nAsk a question (or 'quit'): ")
        if q.lower() == "quit":
            break
        ask(q)