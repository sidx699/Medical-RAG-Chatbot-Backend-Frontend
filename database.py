from langchain_mistralai import MistralAIEmbeddings
from langchain_community.vectorstores import FAISS

vector_store = None

def embeddings_loader():
  embeddings = MistralAIEmbeddings(model="mistral-embed")
  return embeddings

def init_db():
  global vector_store
  embeddings = embeddings_loader()
  vector_store = FAISS.load_local("medical_vector_db", embeddings, allow_dangerous_deserialization=True)

def get_vector_store():
  return vector_store