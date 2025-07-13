# 🧠 Lexi.sg RAG Backend

This project demonstrates a **hybrid Retrieval-Augmented Generation (RAG)** system combining:

- 🔍 **Python (FastAPI + FAISS + Sentence Transformers)**: Handles document embedding, similarity search, and LLM interaction using Ollama.
- ☕ **Spring Boot (Java)**: Acts as the API gateway and provides the unified `/query` route.

🧠 Technologies Used
FastAPI

Sentence Transformers

FAISS

Ollama (TinyLLama)

Spring Boot

Maven



---

## 📁 Project Structure
````
RAG BACKEND/
├── rag-python/ # Python FastAPI backend
│ ├── app.py
│ ├── metadata.json
│ ├── legal_index.faiss
│ ├── requirements.txt
│ └── scripts/
│ └── build_index.py # Script to build FAISS index
│
└── rag-springboot/ # Java Spring Boot project
├── pom.xml
└── src/
└── main/
└── java/
└── dev/anurag/RAG/System/
├── controller/RagController.java
├── service/RagService.java
└── response/RagResponse.java
````

---

## ⚙️ Setup Instructions

### 1️⃣ Prerequisites

- ✅ Python 3.10+
- ✅ Java 17+
- ✅ Ollama installed & working (`https://ollama.com`)
- ✅ Git & Maven

---

### 2️⃣ Python Backend Setup (`rag-python`)

#### 📦 Step 1: Install Dependencies

```bash
cd rag-python
python -m venv venv
venv\Scripts\activate   # or source venv/bin/activate on Linux/Mac

pip install -r requirements.txt
python scripts/build_index.py 
#Chunk and embed sample legal documents from docs/
#Create legal_index.faiss and metadata.json
uvicorn app:app --reload --port 5000

#FastAPI will now be available at:
http://localhost:5000/rag/query
```
3️⃣ Ollama Setup
``ollama run tinyllama
``

### 2️⃣ Java Backend Setup (`rag-java`)
```bash
cd rag-springboot
mvn clean install
mvn spring-boot:run
#Spring Boot will start on:
http://localhost:8080
```
**🧪 How to Test the API**

🔁 API Endpoint

POST http://localhost:8080/query

🔸 Request Body (JSON)

``{
"query": "What is a legal contract?"
}
``

🔹 Response

``{
"answer": "A legal contract is a binding agreement ...",
"citations": [
{
"text": "Some relevant chunk of text ...",
"source": "contract_law.txt"
},
...
]
}
``



**📄 Sample Legal Documents**

You can place .txt legal files in a docs/ folder inside rag-python/ directory. In my code, i provided the folder path of the documents.

Each document will be split into chunks and embedded during the build_index.py script run.



## 📁 Flow of Request
    User->>SpringBoot: POST /query (question)
    SpringBoot->>FastAPI: POST /rag/query (question)
    FastAPI->>FastAPI: Embed question
    FastAPI->>FastAPI: Search FAISS index
    FastAPI->>FastAPI: Build context
    FastAPI->>Ollama: POST /api/chat (prompt)
    Ollama-->>FastAPI: Response (LLM answer)
    FastAPI-->>SpringBoot: JSON { answer, citations }
    SpringBoot-->>User: JSON { answer, citations }

## Architecture Decision
While it's possible to build the entire system in either Spring Boot or Python, this hybrid approach leverages the strengths of both ecosystems to deliver a more modular, efficient, and scalable solution.

 **Reasons for Using Spring Boot (Java):**
Enterprise-level request handling: Spring Boot excels at managing robust, production-grade REST APIs with strong support for dependency injection, validation, and error handling.

Type-safe and maintainable: Java offers strong typing, compile-time checking, and IDE support — making the controller logic highly maintainable and testable.

Easier integration in enterprise environments: Many organizations already use Spring Boot in their backend stack.

 **Reasons for Using FastAPI (Python):**
Seamless integration with AI/ML models: Python has the richest ecosystem for AI/ML tools like sentence-transformers, faiss, and NLP libraries.

Ollama compatibility: The LLM (e.g., tinyllama, mistral) runs natively with Python requests. Python is ideal for constructing and managing LLM prompts and responses.

Rapid prototyping of vector search logic: Using FAISS and Hugging Face models in Python allows fast development and experimentation.












