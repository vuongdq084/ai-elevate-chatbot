"""
Script to build ChromaDB index from existing Git manual chunks.
Run this script after installing ChromaDB to migrate from FAISS to ChromaDB.
"""
 
from context_manager.chroma_context import build_chroma_index
 
def main():
    print("🚀 Building ChromaDB index from Git manual chunks...")
    try:
        build_chroma_index("data/git_manual_chunks", "git_manual")
        print("✅ ChromaDB index built successfully!")
        print("📁 ChromaDB data is stored in './chroma_db' directory")
        print("🎉 You can now use the chatbot with ChromaDB!")
    except Exception as e:
        print(f"❌ Error building ChromaDB index: {e}")
        return 1
    return 0
 
if __name__ == "__main__":
    exit(main())