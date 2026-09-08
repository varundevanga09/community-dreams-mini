import os
import chromadb
from sentence_transformers import SentenceTransformer
from groq import Groq

model = SentenceTransformer("all-MiniLM-L6-v2")
client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_or_create_collection("knowledge_base")
groq_client = Groq(api_key=os.environ["GROQ_API_KEY"])

def ask(question, top_k=3):
    q_embedding = model.encode(question).tolist()
    results = collection.query(query_embeddings=[q_embedding], n_results=top_k)
    retrieved_docs = results["documents"][0]

    context = "\n\n".join(retrieved_docs)
    prompt = f"""Answer the question using ONLY the context below. If the context doesn't contain the answer, say "I don't have enough information."

Context:
{context}

Question: {question}

Answer:"""

    response = groq_client.chat.completions.create(
    model="openai/gpt-oss-20b",
    messages=[{"role": "user", "content": prompt}]
    )
    print("\n--- Retrieved docs ---")
    for d in retrieved_docs:
        print(d[:80], "...")
    print("\n--- Answer ---")
    print(response.choices[0].message.content)

if __name__ == "__main__":
    while True:
        q = input("\nAsk a question (or 'quit'): ")
        if q.lower() == "quit":
            break
        ask(q)