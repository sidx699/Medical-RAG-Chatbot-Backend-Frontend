import os
from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_classic.chains import create_retrieval_chain

def llm_loader():
  llm=ChatMistralAI(model="mistral-large-latest",
    temperature=0.5,
    max_retries=2,)

  return llm

def create_retriever(vector_store):
  retriever=vector_store.as_retriever(search_type="similarity",
    search_kwargs={'k': 4})
  return retriever


def create_prompt():
  template = """You are an assistant for question-answering tasks.
  Use the following pieces of retrieved context to answer the question.
  If you don't know the answer, just say that you don't know.
  Use five sentences maximum and keep the answer concise.

  question: {input}
  context: {context}
  Answer:"""

  prompt = ChatPromptTemplate.from_template(template)
  return prompt


def create_question_answer_chain():
  llm=llm_loader()
  prompt=create_prompt()
  question_answer_chain = create_stuff_documents_chain(llm, prompt)
  return question_answer_chain


def create_rag_chain(vector_store):
  llm=llm_loader()
  retriever=create_retriever(vector_store)
  question_answer_chain=create_question_answer_chain()
  rag_chain = create_retrieval_chain(retriever, question_answer_chain)
  return rag_chain


def generate_response(rag_chain,query):
  response = rag_chain.invoke(query)
  return response["answer"]
