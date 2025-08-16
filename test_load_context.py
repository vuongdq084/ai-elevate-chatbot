import sys
from context_manager.chroma_context import load_context  # đổi 'chroma_index' thành tên file chứa hàm build_chroma_index của bạn

def main():
    print("=== ChromaDB Context Query Tool ===")
    print("Nhập câu hỏi (hoặc gõ 'exit' để thoát)")

    while True:
        question = input("\nCâu hỏi: ").strip()
        if not question:
            continue
        if question.lower() in ["exit", "quit"]:
            print("Thoát.")
            break

        result = load_context(question)

        if result["status"] == "FOUND":
            print("\n--- Context tìm được ---")
            print(result["context"])

            print("\n--- File liên quan ---")
            for file in result["files"]:
                print(f"- {file}")
        else:
            print("⚠ Không tìm thấy context phù hợp.")

if __name__ == "__main__":
    # Nếu muốn nhận câu hỏi qua argument: python test_load_context.py "nội dung câu hỏi"
    if len(sys.argv) > 1:
        question_arg = " ".join(sys.argv[1:])
        result = load_context(question_arg)
        print(result)
    else:
        main()
