# 📄 Document QA System using LlamaIndex & Google Generative AI

An intelligent Question Answering (QA) system that allows users to upload documents (PDF or TXT), ask questions about the content, and receive accurate, AI-powered responses.

## 🚀 Features

* 📁 Upload PDF or TXT files.
* 🤖 Extract and understand content using Google Generative AI and LlamaIndex.
* 🧠 Embedding-based semantic search (FAISS).
* 💬 Ask any question about your document and get context-aware answers.
* 📊 Confidence threshold & response length customization.
* 🎯 Designed for efficient RAG (Retrieval-Augmented Generation) workflows.

---

## 📁 Project Structure

```
QA_WITH_DOC_USING_LLAMA...
├── Data/                        # Contains document files
│   └── MLDOC.txt
├── Experiments/                # For research and testing
│   ├── storage/
│   └── experiment.ipynb
├── QAWithPDF/                  # Core logic for ingestion and QA
│   ├── __init__.py
│   ├── data_ingestion.py
│   └── helper.py
├── storage/                    # Vector store and index files
│   ├── default_vector_store.json
│   ├── docstore.json
│   ├── graph_store.json
│   ├── image_vector_store.json
│   └── index_store.json
├── temp_data/                  # Temporary processed data
├── .env                        # Environment variables
├── requirements.txt            # Project dependencies
├── StreamlitApp.py             # UI using Streamlit
├── setup.py                    # Setup script
├── logger.py                   # Logging configuration
├── exception.py                # Custom exceptions
```

---

## 🧠 Technologies Used

* **Python**
* **Streamlit** – For building the interactive web UI.
* **LlamaIndex (GPT Index)** – For loading, indexing, and querying documents.
* **Google Generative AI** – For embedding and answering.
* **FAISS** – For efficient vector similarity search.
* **dotenv** – For managing environment variables.

---

## ⚙️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/document-qa-system.git
cd document-qa-system
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Setup `.env`

Create a `.env` file with your API keys:

```env
GOOGLE_API_KEY=your_google_api_key
```

Or use the `.env.example` as a template.

---

## ▶️ Run the Application

```bash
streamlit run StreamlitApp.py
```

Open your browser at: [http://localhost:8501]([http://localhost:8501](https://sayedalihassaan-qa-with-doc-using-llamainde-streamlitapp-sg1oen.streamlit.app/))

---

## 📚 How It Works

1. **Upload Document** – PDF or TXT file is loaded.
2. **Text Extraction** – Document content is extracted and split into chunks.
3. **Embedding** – Chunks are embedded using GeminiEmbeddings from Google.
4. **Indexing** – Vector store (FAISS) is created for efficient retrieval.
5. **Question Answering** – User questions are answered using context retrieved from the document.

---

## 💡 Tips for Best Results

* Upload well-structured, clean documents.
* Ask concise, direct questions.
* Try rephrasing if the answer isn't accurate.

---

## 🧪 Example Use Case

**Document:** `MLDOC.txt`
**Question:** *"What is deep learning?"*

**Answer:**

> Deep learning is a subset of machine learning based on artificial neural networks with representation learning. It enables systems to learn from large amounts of data by automatically extracting features.

---

## 🔐 License

MIT License © 2025

---

## 🤝 Contributors

* Eng. Sayed Ali – AI Engineer & Project Lead

---

هل تحب أضيف ملف `README.md` داخل المشروع لك تلقائيًا؟
