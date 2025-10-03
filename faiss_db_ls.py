import faiss 
import numpy as np

d = 512 
nb = 100 
np.random.seed(42)
embeddings = np.random.random((nb, d)).astype("float32")

index = faiss.IndexFlat2(d)
index.add(embeddings)

print("Number of vectors in index:", index.ntotal)

index = faiss.IndexHNSWFlat(d, 32) 
index.add(embeddings)


# create a query vector
query = np.random.random((1, d)).astype('float32')

# search for top 5 nearest neighbors
k = 5
distances, indices = index.search(query, k)
print("Top 5 distances:", distances)
print("Top 5 indices:", indices)
faiss.write_index(index, "faiss_index.idx")
index = faiss.read_index("faiss_index.idx")
