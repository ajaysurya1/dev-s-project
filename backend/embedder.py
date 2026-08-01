from chromadb.utils.embedding_functions import DefaultEmbeddingFunction

embedding_function = DefaultEmbeddingFunction()


def generate_embeddings(text_list):
    embeddings = embedding_function(text_list)
    result = []
    for embedding in embeddings:
        result.append([float(value) for value in embedding])
    return result


def generate_single_embedding(text):
    embeddings = embedding_function([text])
    return [float(value) for value in embeddings[0]]
