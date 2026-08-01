def score_chunk(question, chunk_text):
    question_words = set(question.lower().split())
    chunk_words = set(chunk_text.lower().split())
    if len(question_words) == 0:
        return 0.0
    overlap = question_words.intersection(chunk_words)
    return round(len(overlap) / len(question_words), 4)


def rerank_chunks(question, chunks):
    if not chunks:
        return chunks

    for chunk in chunks:
        keyword_score = score_chunk(question, chunk["text"])
        chunk["score"] = round((chunk["score"] + keyword_score) / 2, 4)

    chunks.sort(key=lambda x: x["score"], reverse=True)
    return chunks


def calculate_confidence(chunks):
    top_chunks = chunks[:3]

    if len(top_chunks) == 0:
        return 0.0

    total = 0
    for chunk in top_chunks:
        total = total + chunk["score"]

    average = total / len(top_chunks)
    confidence = round(average, 2)
    return confidence
