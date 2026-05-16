# ⚖️ Legal Aid Chatbot API (RAG-Powered)

An AI-powered legal assistance chatbot that simplifies complex legal information using Retrieval-Augmented Generation (RAG).

---

## ✨ Features

* AI-powered legal query answering
* Retrieval-Augmented Generation (RAG)
* ChromaDB vector database
* Gemini 2.5 Flash integration
* FastAPI backend
* Semantic document retrieval
* Responsive frontend UI

---

## 🏗️ Project Architecture

The application follows a standard RAG pipeline:

1. Frontend Layer
2. Backend/API Layer
3. Embedding & Vector Database Layer
4. Retrieval & LLM Generation Layer

---

## 🛠️ Tech Stack

| Technology         | Purpose           |
| ------------------ | ----------------- |
| FastAPI            | Backend API       |
| LangChain          | RAG orchestration |
| ChromaDB           | Vector database   |
| HuggingFace BGE-M3 | Embeddings        |
| Gemini 2.5 Flash   | LLM               |
| HTML/CSS/JS        | Frontend          |

---

## 📁 Project Structure

```bash
legal-aid-chatbot/
│
├── static/
├── model.py
├── requirements.txt
└── README.md
```

---

## ⚙️ Installation

```bash
git clone https://github.com/yourusername/legal-aid-chatbot.git

cd legal-aid-chatbot

pip install -r requirements.txt
```

---

## 🚀 Run the Project

```bash
uvicorn model:app --reload
```

---

## 📄 License

MIT License
