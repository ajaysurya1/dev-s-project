import chromadb

client = chromadb.PersistentClient(path="chroma_db")
collection = client.get_or_create_collection(name="documents")


def add_chunks(document_id, chunks, embeddings):
    ids = []
    metadata = []

    for i in range(len(chunks)):
        ids.append(f"{document_id}_chunk_{i}")

        metadata.append({
            "document_id": str(document_id),
            "chunk_index": i
        })

    collection.add(
        ids=ids,
        documents=chunks,
        embeddings=embeddings,
        metadatas=metadata
    )


def query_chunks(question_embedding, document_ids=None, top_k=5):

    where = None

    if document_ids:
        ids = [str(i) for i in document_ids]

        if len(ids) == 1:
            where = {"document_id": ids[0]}
        else:
            where = {"document_id": {"$in": ids}}

    results = collection.query(
        query_embeddings=[question_embedding],
        n_results=top_k,
        where=where,
        include=["documents", "metadatas", "distances"]
    )

    return results


def delete_document_chunks(document_id):

    data = collection.get(
        where={"document_id": str(document_id)}
    )

    if data["ids"]:
        collection.delete(ids=data["ids"])