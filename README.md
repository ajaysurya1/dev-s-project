# DocMind

A document question-answering app. Upload your files and ask questions across them using AI.

I built this using Python, FastAPI for backend, and Streamlit for frontend.

## What features I implemented:

1. **File Upload and Parsing**: Supports PDF, Word (.docx), TXT, CSV, and images (uses OCR if tesseract is installed).
2. **Semantic Chunking**: Uses LangChain RecursiveCharacterTextSplitter to split documents at natural boundaries.
3. **Vector Search**: Embeds chunks using ChromaDB built-in embedding model and stores them for similarity search.
4. **AI Answers**: Sends the top retrieved chunks to Groq (LLaMA 3) to generate a grounded answer.
5. **Reranking**: Blends vector similarity with keyword overlap to surface the most relevant chunks first.
6. **Confidence Score**: Shows an overall confidence percentage after each answer.
7. **Source Citations**: Each answer shows which document it came from, with 5 expandable source excerpts.
8. **Document Management**: View, preview, and delete uploaded documents from the UI.

## Live deployment

- **Frontend**: https://docmind.streamlit.app
- **Backend API**: https://dev-s-project.onrender.com

## Tech stack

| Layer | Technology |
|---|---|
| Frontend | Streamlit |
| Backend | FastAPI + Uvicorn |
| Embeddings | ChromaDB DefaultEmbeddingFunction (all-MiniLM-L6-v2 via ONNX) |
| Vector store | ChromaDB |
| LLM | Groq (LLaMA 3) |
| Chunking | LangChain RecursiveCharacterTextSplitter |
| OCR | Tesseract (optional) |

## Project structure

```
docmind/
  backend/
    main.py          - FastAPI routes
    ingestion.py     - Text extraction for PDF, DOCX, CSV, TXT, images
    chunker.py       - Recursive character splitting
    embedder.py      - Embedding generation
    vector_store.py  - ChromaDB add/query/delete
    retriever.py     - Similarity search
    reranker.py      - Keyword + vector blend reranker
    qa_engine.py     - Groq LLM answer generation
    database.py      - SQLite document metadata
  frontend/
    app.py           - Streamlit entry point
    api_client.py    - HTTP calls to backend
    styles.py        - CSS
    views/
      upload_page.py
      documents_page.py
      ask_page.py
  requirements.txt
  .env               - GROQ_API_KEY (not committed)
```

## Environment variables

Create a .env file in the project root:

```
GROQ_API_KEY=your_groq_api_key_here
```

## Running locally

```
pip install -r requirements.txt

Terminal 1 - backend
cd backend
uvicorn main:app --reload --port 8000

Terminal 2 - frontend
streamlit run frontend/app.py
```
