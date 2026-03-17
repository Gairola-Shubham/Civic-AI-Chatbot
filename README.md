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

# ⚙️ Setup Ollama

Install **Ollama**:

https://ollama.com

Pull the model:
```bash
ollama pull mistral
```

Start the Ollama server before running the chatbot.

---

# 🔒 Why Use Ollama?

Using a local AI model provides:

* 🛜 **Offline AI responses**
* 🔐 **Better privacy (no cloud APIs required)**
* ⚡ **Fast local processing**
* 🧠 **More intelligent responses than keyword search**

---

# 📂 Project Structure
```text
Civic-AI-Chatbot
│
├── scripts/
│ ├── extract_and_clean.py
│ ├── prepare_chunks.py
│ ├── build_vector_db.py
│ ├── query_engine_llm.py
│
├── app.py # Streamlit chatbot interface
├── data_raw/ # Raw PDFs (not uploaded)
├── data_processed/ # Extracted text
├── requirements.txt
└── README.md
```
---

# 📊 Dataset

Civic AI uses publicly available Delhi government data:

- ~2755 PDF documents  
- ~5.6 GB dataset  
- ~129,588 text chunks  

---

# 🌐 Data Sources

Data was collected from official government portals:

### 🏛 Delhi Legislative Assembly
https://delhiassembly.delhi.gov.in  
- Assembly proceedings  
- Questions & answers  
- Budget discussions  

---

### 💰 Budget Documents
- Budget speeches  
- Financial statements  
- Budget summaries  

---

### 🌿 Delhi Pollution Control Committee
https://dpcc.delhigovt.nic.in  
- Air quality reports  
- Pollution monitoring data  

---

### 🚇 Delhi Transport Department
- Electric vehicle policies  
- Transport initiatives  

---

### 📜 Gazette Notifications
- Acts and rules  
- Official notifications  

---

### 🌊 Environmental Reports
- Yamuna river cleaning reports  
- Sewage treatment reports  

---

# 📦 Installation

## 1️⃣ Clone the repository
```bash
git clone https://github.com/your-username/civic-ai-chatbot.git
cd civic-ai-chatbot
```
---

## 2️⃣ Create a virtual environment
```bash
python -m venv venv
```

Activate it

### Windows
```bash
venv\Scripts\activate
```
---

## 3️⃣ Install dependencies
```bash
pip install -r requirements.txt
```

---

## 4️⃣ Install Tesseract OCR

Download and install from:  
https://github.com/tesseract-ocr/tesseract  

Install Hindi language pack as well.

---

## 5️⃣ Run the chatbot
```bash
streamlit run app.py
```

---

# ▶️ Running the Chatbot

Open in browser:
```bash
http://localhost:8501
```

---

# 📌 Example Queries

Civic AI can answer queries such as:

* What is Delhi's education budget for 2024?  
* What measures has Delhi taken to control pollution?  
* What is the Yamuna cleaning plan?  
* Delhi EV policy  
* दिल्ली में शिक्षा बजट कितना है?  

---

# 🧠 How It Works

1. The system processes government PDFs and extracts text.

2. Text is divided into smaller chunks.

3. Each chunk is converted into embeddings.

4. FAISS stores embeddings for fast retrieval.

5. User queries are matched with relevant chunks.

6. The LLM generates answers based on retrieved context.

---

# 🔮 Future Improvements

Possible upgrades for the system:

* 🌐 Online deployment  
* 🔍 Better query filtering  
* 📄 Improved document coverage  
* 💻 Enhanced UI  

---

# 🎯 Purpose of This Project

This project was built to:

* Apply **AI to real-world government data**
* Build a **RAG-based chatbot system**
* Improve **public data accessibility**
* Demonstrate **end-to-end AI pipeline development**

---

# 👥 Team

- Shubham Gairola  
- Amar Bammi  
- Rishita  
