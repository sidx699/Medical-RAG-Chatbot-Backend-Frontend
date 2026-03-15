import utils
import os
from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException
from database import get_vector_store

load_dotenv()
mistral_key = os.getenv("MISTRAL_API_KEY")

if not mistral_key:
    raise ValueError("MISTRAL_API_KEY not found in .env file")

os.environ["MISTRAL_API_KEY"] = mistral_key

router = APIRouter()

rag_chain = None

def get_rag_chain():
    global rag_chain

    if rag_chain is None:
        vector_store = get_vector_store()

        if vector_store is None:
            raise HTTPException(
                status_code=500,
                detail="Vector store not initialized."
            )

        rag_chain = utils.create_rag_chain(vector_store)

    return rag_chain


@router.get("/")
def root():
    return {"message": "Welcome to the Medical RAG Chatbot API"}


@router.post("/query")
async def get_response(query_text: str):

    rag_chain = get_rag_chain()

    question = {
        "input": query_text,
        "context": ""
    }

    response = utils.generate_response(rag_chain, question)

    return {"answer": response}
