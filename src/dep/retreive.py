def query_faiss(query, k=5):
    query_vector = embeddings.embed_query(query)
    docs = faiss_index.similarity_search_by_vector(query_vector, k=k)
    return docs
