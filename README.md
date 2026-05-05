# 🚀 Civic AI – Multi-State Government Transparency Chatbot

## 📌 Overview

Civic AI is an intelligent chatbot system designed to simplify access to complex government data such as economic surveys, budget reports, and policy documents.
It allows users to ask questions in natural language and receive accurate, source-based answers using a combination of retrieval techniques and a local language model.

---

## 🎯 Key Features

* 💬 Natural language query support
* 🔍 Hybrid Retrieval (FAISS + BM25)
* 🧠 Retrieval-Augmented Generation (RAG)
* 🤖 Local LLM (Phi-3 via Ollama)
* 📌 Source-based answers (state, domain, page)
* 👤 User login, signup, and profile management
* 🗂 Chat history support
* ⚡ Fast backend using FastAPI

---

## 🏗 System Architecture

User → Frontend (React) → FastAPI Backend → Hybrid Retrieval (FAISS + BM25) → LLM (Phi-3) → Response

---

## 🧠 How It Works

1. User enters a query in the chat interface
2. Query is sent to backend via REST API
3. Backend processes query using hybrid retrieval:

   * FAISS (semantic search)
   * BM25 (keyword search)
4. Relevant document chunks are retrieved
5. Context is passed to the LLM (Phi-3)
6. LLM generates final response
7. Response + sources displayed to user

---

## ⚙️ Tech Stack

### 🔹 Frontend

* React.js
* HTML, CSS

### 🔹 Backend

* FastAPI (Python)
* REST API

### 🔹 AI / NLP

* Sentence Transformers (E5 Model)
* FAISS (Vector Search)
* BM25 (Keyword Search)
* Ollama (Local LLM - Phi-3)

---

## 📂 Project Structure

```
Civic-AI/
│
├── app.py
├── requirements.txt
├── scripts/
├── frontend/
├── .gitignore
└── README.md
```

---

## 🧪 Installation & Setup

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/your-username/civic-ai.git
cd civic-ai
```

### 2️⃣ Create Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate   # Windows
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Run Backend

```bash
uvicorn app:app --reload
```

### 5️⃣ Run Frontend

```bash
cd frontend
npm install
npm start
```

---

## 📊 Data Sources

We collected data from official government portals to ensure authenticity and reliability:

* Delhi Economic Survey
  https://delhiplanning.delhi.gov.in/

* Ministry of Statistics and Programme Implementation (MOSPI)
  https://mospi.gov.in/

* NITI Aayog Reports
  https://www.niti.gov.in/

* Open Government Data Platform (India)
  https://data.gov.in/

* Ministry of Finance (Budget Data)
  https://www.indiabudget.gov.in/

---

## 📸 Screenshots

> Add your project screenshots here

### 🔹 Login Page

![Login](screenshots/login.png)

### 🔹 Chat Interface

![Chat](screenshots/chat.png)

### 🔹 Profile Page

![Profile](screenshots/profile.png)

### 🔹 Example Response with Sources

![Response](screenshots/response.png)

---

## ⚠️ Limitations

* Limited dataset coverage
* No multilingual support
* Chat history stored locally
* Performance depends on data quality

---

## 🚀 Future Improvements

* 🌐 Multilingual support (Hindi + English)
* 🎙 Voice-based interaction
* ☁ Cloud deployment
* 📈 Automated evaluation metrics
* 🔐 Secure authentication (JWT)

---

## 👨‍💻 Contributors

* Shubham Gairola
* Amar Bammi
* Rishita

---

## 📜 License

This project is developed for academic purposes.

---

## 🙌 Acknowledgements

* FastAPI Documentation
* FAISS Library
* Sentence Transformers
* Ollama (Phi-3 Model)

---
