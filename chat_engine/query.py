from dotenv import load_dotenv
import os

from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langchain_openai import AzureChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import tool
from user_manager.user import get_user_questions_answers

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_API_BASE = os.getenv("OPENAI_API_BASE")
DEPLOYMENT_NAME = "GPT-4o-mini"
 
# Step 1: Init client
llm = AzureChatOpenAI(
    deployment_name=DEPLOYMENT_NAME,
    api_version="2024-07-01-preview",
    api_key=OPENAI_API_KEY,
    azure_endpoint=OPENAI_API_BASE,
    temperature=0.3,
    max_tokens=500
)

# Step 2: Define search tool - mock function
@tool
def search_document(keyword: str) -> str:
    """
    Tìm document phù hợp với keyword từ câu hỏi người dùng. Ví dụ: permission, hệ thống, guideline
    Nếu không có thì trả về 'Không tìm thấy document phù hợp.'
    """
    documents = {
        "permission": "https://github.com/your-org/qna-permission-guideline",
        "hệ thống": "https://github.com/your-org/qna-system-architecture",
        "guideline": "https://github.com/your-org/qna-general-guideline",
        "authentication": "https://github.com/your-org/qna-authentication-flow",
        "authorization": "https://github.com/your-org/qna-authorization-guide",
        "deployment": "https://github.com/your-org/qna-deployment-process",
        "monitoring": "https://github.com/your-org/qna-monitoring-and-alerting",
        "ci/cd": "https://github.com/your-org/qna-cicd-pipeline",
        "backup": "https://github.com/your-org/qna-backup-strategy",
        "logging": "https://github.com/your-org/qna-logging-standard",
        "troubleshooting": "https://github.com/your-org/qna-troubleshooting-guideline",
        "onboarding": "https://github.com/your-org/qna-onboarding-docs",
        "offboarding": "https://github.com/your-org/qna-offboarding-process",
        "environment": "https://github.com/your-org/qna-environment-setup",
        "secrets": "https://github.com/your-org/qna-secret-management",
        "cost": "https://github.com/your-org/qna-cost-optimization",
        "incident": "https://github.com/your-org/qna-incident-response",
        "sla": "https://github.com/your-org/qna-sla-and-slo",
        "security": "https://github.com/your-org/qna-security-guidelines",
        "architecture": "https://github.com/your-org/qna-system-design",
    }
    return documents.get(keyword.lower(), "Không tìm thấy document phù hợp.")

with open('chat_engine/system_prompt.txt','r',encoding = 'utf-8') as f:
    system_prompt = f.read()

prompt = ChatPromptTemplate.from_messages([
   ("system", system_prompt),
    ("human", "{question}")
])

# Define Tool
chat_with_tools = llm.bind_tools([search_document])

def query(user_id, history, context, question):
    # Debug
    built_prompt = prompt.invoke({
        "context": context,
        "history": history,
        "question": question
    })
    print("=== Prompt sent to LLM ===")
    print(built_prompt.to_string())

    # Load user questions & answers
    user_data = get_user_questions_answers(user_id)
    history_messages = []
    if user_data["status"] == "FOUND":
        questions = user_data["questions"]
        answers = user_data["answers"]
        # Chuyển list Q/A thành HumanMessage/AIMessage
        for q, a in zip(questions, answers):
            history_messages.append(HumanMessage(content=q))
            history_messages.append(AIMessage(content=a))

    # Gửi câu hỏi, LLM tự quyết định có gọi tool không
    response = chat_with_tools.invoke([
        SystemMessage(content=context),
        *history_messages,
        HumanMessage(content=question)
    ])

    # Nếu model gọi function, response sẽ có ToolMessage
    if response.tool_calls:
        # Lấy tool_call đầu tiên
        tool_call = response.tool_calls[0]
        if tool_call["name"] == "search_document":
            doc = search_document.invoke(tool_call["args"])
            # Gửi lại để model trả lời thân thiện
            followup = llm.invoke([
                SystemMessage(content="Bạn là trợ lý kỹ thuật hỗ trợ người dùng tìm tài liệu dự án."),
                HumanMessage(content=question),
                AIMessage(content=f"Kết quả tìm thấy: {doc}"),
                HumanMessage(content="Hãy trả lời lại người dùng một cách thân thiện, kèm link nếu có.")
            ])
            return followup.content.strip()
    return response.content.strip()

# Example usage
if __name__ == "__main__":
    print("Q1:", query("test", [], "", "I want to find infomation about álslsflfa inside the project"))
    print("Q2:", query("test", [], "", "What is EC2 auto scaling?"))
    print("Q3:", query("test", [], "", "I want to find infomation about permission inside the project"))