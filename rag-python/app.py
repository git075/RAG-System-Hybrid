from fastapi import FastAPI, Request
from sentence_transformers import SentenceTransformer
import numpy as np
import faiss
import json
import requests

app = FastAPI()

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Load FAISS index
index = faiss.read_index("legal_index.faiss")

# ✅ FIX: open metadata file with UTF-8 encoding
with open("metadata.json", encoding="utf-8") as f:
    metadata = json.load(f)

@app.post("/rag/query")
async def rag_query(req: Request):
    try:
        body = await req.json()
        question = body["query"]

        # Embed the query
        q_embed = model.encode(
            [question],
            normalize_embeddings=True
        ).astype("float32")

        # Search index for top 5 chunks
        D, I = index.search(q_embed, k=5)

        # Retrieve top chunks
        top_chunks = [metadata[i] for i in I[0]]

        # Prepare context for LLM
        context = "\n\n".join(
            [f"{c['text']} (Source: {c['source']})" for c in top_chunks]
        )

        # Construct prompt
        prompt = f"""You are a legal assistant. Answer the following question strictly using only the context provided.

Context:
{context}

Question:
{question}
"""

        # 🔥 Call Ollama with streaming response
        r = requests.post(
            "http://localhost:11434/api/chat",
            json={
                "model": "tinyllama",
                "messages": [
                    {"role": "user", "content": prompt}
                ]
            },
            stream=True
        )

        # 🔥 Read Ollama's streamed JSON lines
        chunks = []
        for line in r.iter_lines():
            if line:
                data = json.loads(line.decode("utf-8"))
                # Check for error
                if "error" in data:
                    return {
                        "error": "Ollama returned an error",
                        "details": data["error"]
                    }
                if "message" in data:
                    chunks.append(data["message"]["content"])

        # Join all partial tokens
        answer = "".join(chunks)

        return {
            "answer": answer,
            "citations": [
                {"text": c["text"], "source": c["source"]}
                for c in top_chunks
            ]
        }

    except Exception as e:
        return {
            "error": "Server error",
            "details": str(e)
        }
