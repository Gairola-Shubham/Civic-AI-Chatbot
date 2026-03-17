# 🏛 Civic AI – Delhi Government Transparency Chatbot

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Platform](https://img.shields.io/badge/Platform-Local%20AI-lightgrey)
![Status](https://img.shields.io/badge/Project-Active-success)

**Civic AI** is a lightweight **AI-powered document chatbot** that enables users to query **Delhi government data** using natural language.

It processes thousands of official PDFs and uses **semantic search + AI (LLM)** to retrieve accurate answers along with document sources.

This project demonstrates how to combine **OCR, embeddings, vector databases, and language models** to build a real-world AI system.

---

# 🎥 Example Interaction

**User**: What is Delhi's education budget for 2024?

**Assistant**: The Delhi government allocated approximately 21.57% of its total budget to education in 2024.

**Source**: Budget Speech 2024–25

---

# ✨ Features

### 🔍 Semantic Search

* Finds relevant information using **meaning-based search**, not just keywords

### 🤖 AI Answer Generation

* Uses **Mistral LLM** to generate human-like responses

### 🌐 Multilingual Support

* Supports both **Hindi and English queries**

### 📄 Source Citation

* Displays document references for transparency

### 💻 Web Chatbot Interface

* Built using **Streamlit**

### ⚡ Fast Retrieval

* Uses **FAISS vector database** for efficient search

---

# 🏗️ Architecture

Civic AI follows a **Retrieval-Augmented Generation (RAG)** pipeline:

```
Government PDFs
↓
OCR (Tesseract)
↓
Text Extraction
↓
Text Chunking
↓
Embedding Model
↓
FAISS Vector Database
↓
LLM (Mistral via Ollama)
↓
Streamlit Chatbot
```
---

# ⚙️ Technologies Used

| Technology              | Purpose                          |
|------------------------|----------------------------------|
| Python                 | Core programming language        |
| PyMuPDF                | PDF text extraction              |
| Tesseract OCR          | Extract text from scanned PDFs   |
| Sentence Transformers  | Generate embeddings              |
| FAISS                  | Vector similarity search         |
| Ollama                 | Run LLM locally                  |
| Mistral                | Language model                   |
| Streamlit              | Web interface                    |

---

# 🧠 AI Integration (Ollama)

Civic AI uses a **local AI model** powered by **Ollama**.

This allows the chatbot to behave like a real AI system instead of relying only on predefined responses.

### Example

**User:**
What is Delhi's EV policy?

**Assistant:**
Delhi's Electric Vehicle Policy focuses on promoting electric mobility, reducing pollution, and providing incentives for EV adoption.

---

## ⚙️ Setup Ollama

Install **Ollama**:

https://ollama.com

Pull the model:
ollama pull mistral
