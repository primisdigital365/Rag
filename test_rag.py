import os
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

# Load the vector store
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

db = FAISS.load_local(
    "vectorstore",
    embeddings,
    allow_dangerous_deserialization=True
)

# Test query
query = "this is proved ai base service"

print(f"🔍 Testing query: {query}\n")

# Get similar documents
docs = db.similarity_search(query, k=5)

print(f"📄 Found {len(docs)} relevant chunks:\n")
print("=" * 80)

for i, doc in enumerate(docs, 1):
    print(f"\n--- Chunk {i} ---")
    print(doc.page_content[:300])  # Show first 300 chars
    print("...")

# Also try with scores
docs_with_scores = db.similarity_search_with_score(query, k=5)

print("\n\n📊 Similarity Scores:")
print("=" * 80)
for doc, score in docs_with_scores:
    print(f"Score: {score:.4f}")
    print(f"Content preview: {doc.page_content[:100]}...\n")