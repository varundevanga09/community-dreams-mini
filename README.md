<div align="center">

<img src="https://readme-typing-svg.demolab.com?font=Fira+Code&size=24&pause=1000&color=2E86AB&center=true&vCenter=true&width=600&lines=Community+Dreams+Mini;RAG+Pipeline+%2B+LangGraph+%2B+Redis+Cache;Built+from+scratch+in+5+days" alt="Typing SVG" />

# 🌱 Community Dreams — Mini

A small, self-contained Retrieval-Augmented Generation (RAG) system I built to properly understand — from the ground up — the architecture behind a production AI platform I worked on. Runs entirely on free/local tooling.

![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=flat-square&logo=python&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-Orchestration-1C3C3C?style=flat-square)
![LangGraph](https://img.shields.io/badge/LangGraph-Multi--Agent-1C3C3C?style=flat-square)
![ChromaDB](https://img.shields.io/badge/ChromaDB-Vector%20Store-FF6F00?style=flat-square)
![Redis](https://img.shields.io/badge/Redis-Caching-DC382D?style=flat-square&logo=redis&logoColor=white)
![Groq](https://img.shields.io/badge/Groq-LLM%20Inference-F55036?style=flat-square)
![Status](https://img.shields.io/badge/status-in%20progress-yellow?style=flat-square)

</div>

---

## Why I built this

I worked on the AI platform at **Community Dreams Foundation**, but wanted to rebuild the core architecture myself — end to end, one piece at a time — to make sure I actually understand *why* each component exists, not just that it does. This repo is that rebuild: a working RAG pipeline with semantic re-ranking, LangGraph orchestration, and Redis caching, built over five focused days.

Everything here runs for **$0** — no paid APIs, no cloud infra, no credit card.

---

## Build progress

*Updated as I complete each day — this reflects what's actually working right now, not the finished target.*

- [x] Day 1 — RAG pipeline: embed → retrieve → generate (ChromaDB + Groq)
- [ ] Day 2 — Semantic re-ranking (cross-encoder)
- [ ] Day 3 — LangGraph orchestration + confidence-based fallback
- [ ] Day 4 — Redis caching + evaluation harness
- [ ] Day 5 — Polish, real measured results, public release

---

## Architecture

```
User Question
     │
     ▼
Embed Query (sentence-transformers)
     │
     ▼
Vector Search — top-K candidates (ChromaDB)
     │
     ▼
Semantic Re-ranking — cross-encoder scoring
     │
     ▼
Redis Cache Check ── hit ──► Return cached answer
     │ miss
     ▼
LangGraph Orchestration
  ├─ confidence check (low score → fallback, no guessing)
  └─ LLM generation (Groq — Llama/GPT-OSS)
     │
     ▼
Answer + cache write
```

---

## What each piece does

| Component | Tool | Purpose |
|---|---|---|
| Embeddings | `sentence-transformers` (`all-MiniLM-L6-v2`) | Converts text to vectors so meaning, not just keywords, can be searched |
| Vector store | ChromaDB | Stores document embeddings, retrieves nearest matches to a query |
| Re-ranking | Cross-encoder (`ms-marco-MiniLM-L-6-v2`) | Re-scores retrieved candidates for true relevance before they reach the LLM |
| Orchestration | LangGraph | State machine with a conditional branch — low-confidence retrieval routes to a fallback instead of letting the model guess |
| Caching | Redis | Repeated questions are served from cache instead of re-running the full pipeline |
| Generation | Groq API (free tier) | Hosted LLM inference — no local GPU required |

---

## Results (measured on my own test set)

> *Filled in as I complete each day of the build — real numbers from my own eval harness, not borrowed ones.*

- Retrieval accuracy (top-5 contains correct doc): `TBD`
- Answer accuracy on 20-question eval set: `TBD`
- Re-ranking impact (before → after): `TBD`
- Cache hit latency vs. full pipeline latency: `TBD`

---

## Running it locally

```bash
git clone https://github.com/varundevanga09/community-dreams-mini.git
cd community-dreams-mini
pip install -r requirements.txt

export GROQ_API_KEY="your-groq-key"   # free at console.groq.com

python make_docs.py   # generates the sample knowledge base
python ingest.py      # embeds docs into ChromaDB
python query.py       # ask it a question
```

---

## What I learned building this

- How vector similarity search actually works under the hood (cosine similarity, not magic)
- Why re-ranking exists as a separate step from retrieval, and when it changes the outcome
- How to design a system that says "I don't know" instead of hallucinating — via a conditional branch in LangGraph
- The real cost/latency tradeoff caching solves, measured on my own runs

---

<div align="center">

*Built by [Varun Devanga](https://github.com/varundevanga09) — AWS Certified Cloud Architect, MSc Computer Science, CSU Channel Islands*

</div>
