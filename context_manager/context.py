import os
from typing import Dict, List
from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS  # ✅ đúng import
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain.docstore.document import Document

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_API_BASE = os.getenv("OPENAI_API_BASE")

# ✅ Load all .txt documents from folder (including subfolders)
def load_documents_from_folder(folder_path: str) -> List[Document]:
    documents = []
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".txt"):
                full_path = os.path.join(root, file)
                loader = TextLoader(full_path)
                docs = loader.load()
                documents.extend(docs)
    return documents

# ✅ Build FAISS index from documents and save locally
def build_faiss_index(folder_path: str, index_path: str = "faiss_index"):
    documents = load_documents_from_folder(folder_path)

    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_documents(documents)

    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-small",
        openai_api_key=OPENAI_API_KEY,
        openai_api_base=OPENAI_API_BASE
    )
    vectorstore = FAISS.from_documents(chunks, embeddings)
    vectorstore.save_local(index_path)
    print(f"FAISS index saved to: {index_path}")

# ✅ Load relevant context from FAISS index based on a question
def load_context(question: str) -> Dict:
    try:
        embeddings = OpenAIEmbeddings(
            model="text-embedding-3-small",
            openai_api_key=OPENAI_API_KEY,
            openai_api_base=OPENAI_API_BASE
        )
        vectorstore = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)

        docs = vectorstore.similarity_search(question, k=3)
        context = "\n".join([doc.page_content for doc in docs])

        return {"status": "FOUND", "context": context} if context else {"status": "NOT_FOUND", "context": ""}
    except Exception as e:
        print(f"Error loading context: {e}")
        return {"status": "NOT_FOUND", "context": ""}
