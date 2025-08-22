import os
from typing import Dict, List
from dotenv import load_dotenv
import chromadb
from chromadb.config import Settings
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain.docstore.document import Document
 
load_dotenv()
 
OPENAI_API_EMBEDDING_KEY = os.getenv("OPENAI_API_EMBEDDING_KEY")
OPENAI_API_BASE = os.getenv("OPENAI_API_BASE")
 
# ✅ Load all .txt documents from folder (including subfolders)
def load_documents_from_folder(folder_path: str) -> List[Document]:
    documents = []
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".txt"):
                full_path = os.path.join(root, file)
                try:
                    # Use encoding="utf-8" to avoid encoding issues
                    loader = TextLoader(full_path, encoding="utf-8")
                    docs = loader.load()
                    documents.extend(docs)
                except Exception as e:
                    print(f"Warning: Could not load {full_path}: {e}")
    return documents
 
# ✅ Build ChromaDB index from documents and save locally
def build_chroma_index(folder_path: str, collection_name: str = "git_manual"):
    documents = load_documents_from_folder(folder_path)
 
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = splitter.split_documents(documents)
 
    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-small",
        openai_api_key=OPENAI_API_EMBEDDING_KEY,
        openai_api_base=OPENAI_API_BASE
    )
 
    # Initialize ChromaDB client with explicit local settings
    try:
        client = chromadb.PersistentClient(path="./chroma_db", settings=Settings(allow_reset=True))
        # Remove collection if exists
        try:
            client.delete_collection(name=collection_name)
        except Exception as e:
            print(f"Info: Could not delete collection (may not exist): {e}")
        collection = client.create_collection(name=collection_name)
    except Exception as e:
        print(f"ChromaDB connection/init error: {e}")
        raise
   
    # Prepare documents for ChromaDB
    documents_text = [chunk.page_content for chunk in chunks]
    metadatas = [{"source": chunk.metadata.get("source", "unknown")} for chunk in chunks]
    ids = [f"chunk_{i}" for i in range(len(chunks))]
   
    # Get embeddings with error handling
    try:
        print(f"[DEBUG] Generating embeddings for {len(documents_text)} chunks...")
        embeddings_list = embeddings.embed_documents(documents_text)
        print("[DEBUG] Embeddings generated successfully.")
    except Exception as e:
        print(f"[ERROR] Failed to generate embeddings: {e}")
        raise
 
    # Add to collection
    try:
        collection.add(
            embeddings=embeddings_list,
            documents=documents_text,
            metadatas=metadatas,
            ids=ids
        )
        print(f"ChromaDB collection '{collection_name}' created with {len(chunks)} chunks")
    except Exception as e:
        print(f"[ERROR] Failed to add documents to ChromaDB: {e}")
        raise
 
# ✅ Load relevant context from ChromaDB based on a question
def load_context(question: str, collection_name: str = "git_manual") -> Dict:
    try:
        embeddings = OpenAIEmbeddings(
            model="text-embedding-3-small",
            openai_api_key=OPENAI_API_EMBEDDING_KEY,
            openai_api_base=OPENAI_API_BASE
        )
       
        # Initialize ChromaDB client
        try:
            client = chromadb.PersistentClient(path="./chroma_db", settings=Settings(allow_reset=True))
            collection = client.get_collection(name=collection_name)
        except Exception as e:
            print(f"ChromaDB connection/init error: {e}")
            return {"status": "NOT_FOUND", "context": "", "files": []}
       
        # Get embedding for the question
        question_embedding = embeddings.embed_query(question)
       
        # Search for similar documents
        results = collection.query(
            query_embeddings=[question_embedding],
            n_results=5
        )
       
        # Extract documents
        documents = results["documents"][0] if results["documents"] else []
        context = "\n".join(documents)

        # Extract unique file names from metadata
        metadatas = results["metadatas"][0] if results["metadatas"] else []
        seen = set()
        files = []
        for m in metadatas:
            src = m.get("source", "unknown")
            if src not in seen:
                seen.add(src)
                files.append(src)

        return {
            "status": "FOUND" if context else "NOT_FOUND",
            "context": context,
            "files": files
        }
    except Exception as e:
        print(f"Error loading context: {e}")
        return {"status": "NOT_FOUND", "context": "", "files": []}