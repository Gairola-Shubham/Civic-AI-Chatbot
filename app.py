import streamlit as st
import json
import faiss
import requests
from sentence_transformers import SentenceTransformer

INDEX_FILE = "faiss_index.bin"
CHUNKS_FILE = "data_chunks.json"
TOP_K = 5
SIMILARITY_THRESHOLD = 0.35

st.set_page_config(
    page_title="Civic AI - Delhi Government Chatbot",
    layout="wide"
)

st.title("🏛 Civic AI — Delhi Government Transparency Assistant")

st.markdown(
"""
Ask questions about:

• Delhi Budget  
• Pollution policies  
• Assembly discussions  
• Transport initiatives  
• Government programs  
"""
)

# Sidebar example queries
st.sidebar.header("Example Questions")

st.sidebar.markdown("""
• What is Delhi's education budget for 2024?  
• What measures has Delhi taken to control pollution?  
• What is the Yamuna river rejuvenation plan?  
• Delhi electric vehicle policy  
• दिल्ली में शिक्षा बजट कितना है?
""")

# Load model
@st.cache_resource
def load_model():
    return SentenceTransformer("intfloat/multilingual-e5-base")

# Load FAISS index
@st.cache_resource
def load_index():
    return faiss.read_index(INDEX_FILE)

# Load chunks
@st.cache_resource
def load_chunks():
    with open(CHUNKS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

model = load_model()
index = load_index()
chunks = load_chunks()

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Search function
def search_documents(query, top_k=TOP_K):

    query_embedding = model.encode(
        ["query: " + query],
        normalize_embeddings=True
    )

    scores, indices = index.search(query_embedding, top_k)

    results = []

    for score, i in zip(scores[0], indices[0]):

        if score < SIMILARITY_THRESHOLD:
            continue

        chunk = chunks[i]

        results.append({
            "text": chunk["text"],
            "source_file": chunk["source_file"],
            "source_path": chunk["source_path"],
            "score": float(score)
        })

    return results


# LLM call
def ask_llm(question, context):

    prompt = f"""
You are CivicAI, a chatbot that answers questions using Delhi Government documents.

RULES:
- Use ONLY the provided context.
- If the answer is not in the context, say:
"The information is not available in the dataset."
- Do not guess or use outside knowledge.

Context:
{context}

Question:
{question}

Provide a clear answer and mention the document source.
"""

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "mistral",
            "prompt": prompt,
            "stream": False
        }
    )

    return response.json()["response"]


# Chat input
if prompt := st.chat_input("Ask a question about Delhi governance"):

    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):

        with st.spinner("Searching documents..."):

            results = search_documents(prompt)

            if len(results) == 0:
                answer = "The information is not available in the dataset."
                st.markdown(answer)

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer
                })

                st.stop()

            context = "\n\n".join([r["text"] for r in results])

            answer = ask_llm(prompt, context)

            st.markdown(answer)

            st.session_state.messages.append({
                "role": "assistant",
                "content": answer
            })

            st.divider()

            st.subheader("Sources")

            for r in results:
                with st.expander(r["source_file"]):
                    st.write(r["text"][:800])
                    st.caption(r["source_path"])