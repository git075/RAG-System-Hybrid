import os
import json
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from docx import Document
import fitz  # PyMuPDF

# Load a free embedding model from Hugging Face
model = SentenceTransformer("all-MiniLM-L6-v2")
dimension = 384
index = faiss.IndexFlatIP(dimension)

metadata = []
chunk_size = 500

def chunk_text(text, size=500):
    return [text[i:i+size] for i in range(0, len(text), size)]

def process_docx(file_path, source_name):
    print(f"Processing DOCX: {source_name}")
    doc = Document(file_path)
    text = "\n".join([para.text for para in doc.paragraphs])
    if not text.strip():
        print(f"️ Empty DOCX file: {source_name}")
        return
    chunks = chunk_text(text, chunk_size)
    embeddings = model.encode(chunks, normalize_embeddings=True)
    for i, chunk in enumerate(chunks):
        metadata.append({
            "chunk_id": len(metadata),
            "text": chunk,
            "source": source_name
        })
    index.add(np.array(embeddings, dtype="float32"))

def process_pdf(file_path, source_name):
    print(f"Processing PDF: {source_name}")
    text = ""
    try:
        with fitz.open(file_path) as doc:
            for page in doc:
                text += page.get_text()
    except Exception as e:
        print(f"️ Failed to read PDF {source_name}: {e}")
        return
    if not text.strip():
        print(f"️ Empty PDF file: {source_name}")
        return
    chunks = chunk_text(text, chunk_size)
    embeddings = model.encode(chunks, normalize_embeddings=True)
    for i, chunk in enumerate(chunks):
        metadata.append({
            "chunk_id": len(metadata),
            "text": chunk,
            "source": source_name
        })
    index.add(np.array(embeddings, dtype="float32"))


folder_path = r"D:\DOWNLOADSNEW\InternAssignments\cases\cases"

for filename in os.listdir(folder_path):
    path = os.path.join(folder_path, filename)
    if filename.lower().endswith(".docx"):
        process_docx(path, filename)
    elif filename.lower().endswith(".pdf"):
        process_pdf(path, filename)
    else:
        print(f"Skipping unsupported file: {filename}")

faiss.write_index(index, "legal_index.faiss")
with open("../metadata.json", "w", encoding="utf-8") as f:
    json.dump(metadata, f, indent=2, ensure_ascii=False)

print("Index built successfully!")
