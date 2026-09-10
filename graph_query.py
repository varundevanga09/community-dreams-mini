import os
import re
from typing import TypedDict
import chromadb
from sentence_transformers import SentenceTransformer, CrossEncoder
from groq import Groq
from langgraph.graph import StateGraph, END

# --- Setup (same as before) ---
model = SentenceTransformer("all-MiniLM-L6-v2")
reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")
client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_or_create_collection("knowledge_base")
groq_client = Groq(api_key=os.environ["GROQ_API_KEY"])

CONFIDENCE_THRESHOLD = -5.0  # tune this after testing

def clean_answer(text):
    return re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL).strip()

# --- State definition ---
class GraphState(TypedDict):
    question: str
    candidates: list
    reranked_docs: list
    top_score: float
    answer: str

# --- Nodes ---
def retrieve_node(state: GraphState) -> GraphState:
    q_embedding = model.encode(state["question"]).tolist()
    results = collection.query(query_embeddings=[q_embedding], n_results=8)
    state["candidates"] = results["documents"][0]
    return state

def rerank_node(state: GraphState) -> GraphState:
    pairs = [[state["question"], doc] for doc in state["candidates"]]
    scores = reranker.predict(pairs)
    scored = sorted(zip(state["candidates"], scores), key=lambda x: x[1], reverse=True)

    print("\n--- Re-rank scores ---")
    for doc, score in scored:
        print(f"{score:.3f} | {doc[:60]}...")

    state["reranked_docs"] = [doc for doc, score in scored[:3]]
    state["top_score"] = float(scored[0][1])
    return state

def confidence_check(state: GraphState) -> str:
    # Conditional edge: returns the name of the next node
    if state["top_score"] < CONFIDENCE_THRESHOLD:
        return "fallback"
    return "generate"

def fallback_node(state: GraphState) -> GraphState:
    state["answer"] = "I don't have enough information to answer that confidently."
    return state

def generate_node(state: GraphState) -> GraphState:
    context = "\n\n".join(state["reranked_docs"])
    prompt = f"""You are a community information assistant relaying general educational guidance that has already been reviewed. This is not a diagnosis and you are not creating new medical advice — you are only summarizing the pre-approved reference material below.

Answer the question using ONLY the information in the reference material. If the material doesn't cover it, say "I don't have enough information."

Reference material:
{context}

Question: {state["question"]}

Answer:"""

    response = groq_client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=300
    )
    state["answer"] = clean_answer(response.choices[0].message.content)
    return state

# --- Build the graph ---
graph = StateGraph(GraphState)
graph.add_node("retrieve", retrieve_node)
graph.add_node("rerank", rerank_node)
graph.add_node("generate", generate_node)
graph.add_node("fallback", fallback_node)

graph.set_entry_point("retrieve")
graph.add_edge("retrieve", "rerank")
graph.add_conditional_edges("rerank", confidence_check, {
    "generate": "generate",
    "fallback": "fallback"
})
graph.add_edge("generate", END)
graph.add_edge("fallback", END)

app = graph.compile()

# --- Run loop ---
if __name__ == "__main__":
    while True:
        q = input("\nAsk a question (or 'quit'): ")
        if q.lower() == "quit":
            break
        result = app.invoke({"question": q})
        print("\n--- Answer ---")
        print(result["answer"])