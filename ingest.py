import os
import re
from dotenv import load_dotenv
from supabase import create_client
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import SupabaseVectorStore

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_KEY")

print("🚀 Starting ingestion...")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
embeddings = HuggingFaceEmbeddings(
    model_name="BAAI/bge-m3", model_kwargs={"token": os.getenv("HF_TOKEN")}
)

vector_store = SupabaseVectorStore(
    client=supabase,
    embedding=embeddings,
    table_name="documents",
    query_name="match_documents",
)

# Load documents
loader = DirectoryLoader(
    "data/", glob="**/*.*", loader_cls=TextLoader, silent_errors=True
)
docs = loader.load()
print(f"Loaded {len(docs)} documents")

# Clean and split
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
chunks = text_splitter.split_documents(docs)

print(f"Split into {len(chunks)} chunks. Inserting...")

for i, chunk in enumerate(chunks):
    try:
        vector_store.add_documents([chunk])
        if (i + 1) % 20 == 0:
            print(f"  Inserted {i+1}/{len(chunks)}")
    except Exception as e:
        print(f"Error on chunk {i}: {e}")

print("✅ Ingestion completed!")
