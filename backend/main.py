import os
import sys

sys.path.append(os.path.dirname(__file__))

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

from database import setup_database, save_document, get_all_documents, get_document_by_id, delete_document
from ingestion import extract_text
from chunker import split_text_into_chunks
from embedder import generate_embeddings
from vector_store import add_chunks, delete_document_chunks
from retriever import retrieve_relevant_chunks
from qa_engine import generate_answer
from reranker import rerank_chunks, calculate_confidence

UPLOADS_FOLDER = "uploads"
os.makedirs(UPLOADS_FOLDER, exist_ok=True)
setup_database()

app = FastAPI(title="DocMind API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

ALLOWED_FILE_TYPES = ["pdf", "docx", "txt", "csv", "png", "jpg", "jpeg"]


class QueryRequest(BaseModel):
    question: str
    document_ids: Optional[List[int]] = None


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    file_name = file.filename
    file_extension = file_name.split(".")[-1].lower()

    if file_extension not in ALLOWED_FILE_TYPES:
        raise HTTPException(status_code=400, detail="File type not supported.")

    file_path = os.path.join(UPLOADS_FOLDER, file_name)

    file_content = await file.read()
    with open(file_path, "wb") as saved_file:
        saved_file.write(file_content)

    file_size = os.path.getsize(file_path)

    extracted_text = extract_text(file_path, file_extension)

    if not extracted_text.strip():
        raise HTTPException(status_code=400, detail="No text could be extracted from this file.")

    chunks = split_text_into_chunks(extracted_text)
    embeddings = generate_embeddings(chunks)

    document_id = save_document(file_name, file_extension, file_size, len(chunks), extracted_text)
    add_chunks(document_id, chunks, embeddings)

    return {
        "document_id": document_id,
        "name": file_name,
        "chunk_count": len(chunks),
        "message": "File uploaded and processed successfully."
    }


@app.get("/documents")
def list_documents():
    return get_all_documents()


@app.get("/documents/{document_id}/preview")
def preview_document(document_id: int):
    document = get_document_by_id(document_id)

    if not document:
        raise HTTPException(status_code=404, detail="Document not found.")

    return {
        "name": document["name"],
        "extracted_text": document["extracted_text"],
        "chunk_count": document["chunk_count"],
        "character_count": len(document["extracted_text"])
    }


@app.delete("/documents/{document_id}")
def remove_document(document_id: int):
    document = get_document_by_id(document_id)

    if not document:
        raise HTTPException(status_code=404, detail="Document not found.")

    file_path = os.path.join(UPLOADS_FOLDER, document["name"])
    if os.path.exists(file_path):
        os.remove(file_path)

    delete_document_chunks(document_id)
    delete_document(document_id)

    return {"message": "Document deleted successfully."}


@app.post("/query")
def query_documents(request: QueryRequest):
    if not request.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty.")

    relevant_chunks = retrieve_relevant_chunks(request.question, request.document_ids)

    if not relevant_chunks:
        return {
            "answer": "No relevant content found in the selected documents.",
            "confidence": 0.0,
            "sources": []
        }

    relevant_chunks = rerank_chunks(request.question, relevant_chunks)

    confidence = calculate_confidence(relevant_chunks)

    answer = generate_answer(request.question, relevant_chunks)

    sources = []
    for chunk in relevant_chunks:
        document = get_document_by_id(chunk["document_id"])
        if document:
            sources.append({
                "document_name": document["name"],
                "chunk_index": chunk["chunk_index"],
                "relevance_score": chunk["score"],
                "excerpt": chunk["text"][:250]
            })

    return {
        "answer": answer,
        "confidence": confidence,
        "sources": sources
    }
