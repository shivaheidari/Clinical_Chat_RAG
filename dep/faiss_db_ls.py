import faiss 
import numpy as np

from datasets import load_dataset
from sentence_transformers import SentenceTransformer

pubmedqa = load_dataset("pubmed_qa", "pqa_labeled")
print(pubmedqa["train"][0])
model = SentenceTransformer("all-MiniLM-L6-v2")