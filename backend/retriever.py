from embedder import generate_single_embedding
from vector_store import query_chunks
def retrieve_relevant_chunks(question, document_ids=None, top_k=5):
    embedding = generate_single_embedding(question)

    results = query_chunks(embedding, document_ids, top_k)
    chunks = []
    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

    for text, metadata, distance in zip(documents, metadatas, distances):
        chunks.append({
            "text": text,
            "document_id": int(metadata["document_id"]),
            "chunk_index": metadata["chunk_index"],
            "score": round(1 - distance, 4)
        })

    return chunks