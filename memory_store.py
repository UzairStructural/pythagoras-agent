import openai
import faiss
import pickle
import os
from sentence_transformers import SentenceTransformer

DB_PATH = "embeddings/index.pkl"
model = SentenceTransformer('all-MiniLM-L6-v2')

if os.path.exists(DB_PATH):
    with open(DB_PATH, "rb") as f:
        index, texts = pickle.load(f)
else:
    index = faiss.IndexFlatL2(384)
    texts = []

def store_embedding(text):
    global texts
    vec = model.encode([text])
    index.add(vec)
    texts.append(text)
    with open(DB_PATH, "wb") as f:
        pickle.dump((index, texts), f)

def retrieve_similar_chunks(query, top_k=5):
    vec = model.encode([query])
    D, I = index.search(vec, top_k)
    return "\n\n".join([texts[i] for i in I[0] if i < len(texts)])

