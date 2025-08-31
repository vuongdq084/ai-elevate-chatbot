from dotenv import load_dotenv
import os
from langdetect import detect, LangDetectException

from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langchain_openai import AzureChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import tool
from core.user_manager.user import get_user_questions_answers

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
    CRITICAL: You MUST call this tool whenever a user asks about project-specific topics.
    
    This tool searches for official project documentation. Call it for ANY of these topics:
    
    ENGLISH KEYWORDS:
    - system, permission, deployment, monitoring, authentication, authorization
    - guideline, backup, logging, troubleshooting, onboarding, offboarding
    - environment, secrets, cost, incident, sla, security, architecture, ci/cd
    
    VIETNAMESE KEYWORDS:
    - hệ thống, quyền hạn, triển khai, giám sát, xác thực, ủy quyền
    - hướng dẫn, backup, ghi log, xử lý sự cố, onboarding, offboarding
    - môi trường, bí mật, chi phí, sự cố, bảo mật, kiến trúc
    
    Examples of when to call: 
    - English: "system", "permission", "deployment"
    - Vietnamese: "hệ thống", "quyền hạn", "triển khai"
    
    Input: Extract the main topic keyword from user's question (any language)
    Output: URL to official documentation or "No matching document found"
    
    NEVER skip calling this tool for project topics - it's mandatory!
    """
    # Bilingual keyword mapping - support both English and Vietnamese
    documents = {
        # English keywords
        "permission": "https://github.com/your-org/qna-permission-guideline",
        "system": "https://github.com/your-org/qna-system-architecture",
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
        
        # Vietnamese keywords - map to same documents
        "hệ thống": "https://github.com/your-org/qna-system-architecture",
        "quyền hạn": "https://github.com/your-org/qna-permission-guideline",
        "hướng dẫn": "https://github.com/your-org/qna-general-guideline",
        "xác thực": "https://github.com/your-org/qna-authentication-flow",
        "ủy quyền": "https://github.com/your-org/qna-authorization-guide",
        "triển khai": "https://github.com/your-org/qna-deployment-process",
        "giám sát": "https://github.com/your-org/qna-monitoring-and-alerting",
        "backup": "https://github.com/your-org/qna-backup-strategy",
        "ghi log": "https://github.com/your-org/qna-logging-standard",
        "xử lý sự cố": "https://github.com/your-org/qna-troubleshooting-guideline",
        "onboarding": "https://github.com/your-org/qna-onboarding-docs",
        "offboarding": "https://github.com/your-org/qna-offboarding-process",
        "môi trường": "https://github.com/your-org/qna-environment-setup",
        "bí mật": "https://github.com/your-org/qna-secret-management",
        "chi phí": "https://github.com/your-org/qna-cost-optimization",
        "sự cố": "https://github.com/your-org/qna-incident-response",
        "bảo mật": "https://github.com/your-org/qna-security-guidelines",
        "kiến trúc": "https://github.com/your-org/qna-system-design",
    }
    return documents.get(keyword.lower(), "No matching document found.")

# Load system prompt
current_dir = os.path.dirname(os.path.abspath(__file__))
system_prompt_path = os.path.join(current_dir, 'system_prompt.txt')

try:
    with open(system_prompt_path, 'r', encoding='utf-8') as f:
        system_prompt_template = f.read()
except FileNotFoundError:
    print(f"Error: system_prompt.txt not found at {system_prompt_path}")
    print(f"Current directory: {current_dir}")
    print(f"Files in directory: {os.listdir(current_dir)}")
    raise

# Define Tool
chat_with_tools = llm.bind_tools([search_document])

def detect_language(text):
    """
    Detects the language of a given text.
    Returns 'vi' for Vietnamese or 'en' for English.
    Defaults to 'en' if detection fails or the language is not supported.
    """
    try:
        lang = detect(text)
        if lang == 'vi':
            return 'vi'
        # Default to English for any other detected language
        return 'en'
    except LangDetectException:
        # If detection fails (e.g., for very short/ambiguous text), default to English
        print("Language detection failed, defaulting to English.")
        return 'en'

def query(user_id, history, context, question):
    # Debug context loading
    print(f"=== Context Debug ===")
    print(f"Context length: {len(context) if context else 0}")
    print(f"Context content: {context[:200] if context else 'None'}...")
    
    system_prompt = system_prompt_template.format(context=context)

    # Debug
    
    print("=== System Message sent to LLM ===")
    print(system_prompt)
    print("=== User Message ===")
    print(question)
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
        SystemMessage(content=system_prompt),
        *history_messages,
        HumanMessage(content=question)
    ])

    # Nếu model gọi function, response sẽ có ToolMessage
    if response.tool_calls:
        # Lấy tool_call đầu tiên
        tool_call = response.tool_calls[0]
        if tool_call["name"] == "search_document":
            doc = search_document.invoke(tool_call["args"])
            # Detect language and create language-appropriate followup prompt
            detected_lang = detect_language(question)
            
            if detected_lang == 'vi':
                system_prompt_followup = "Bạn là trợ lý kỹ thuật hỗ trợ người dùng tìm tài liệu dự án."
                result_text = f"Kết quả tìm thấy: {doc}"
                instruction_text = "Hãy trả lời lại người dùng một cách thân thiện, kèm link nếu có."
            else:
                system_prompt_followup = "You are a technical support assistant helping users find project documents."
                result_text = f"Document found: {doc}"
                instruction_text = "Please respond to the user in a friendly manner, including links if available."
            
            # Gửi lại để model trả lời thân thiện
            followup = llm.invoke([
                SystemMessage(content=system_prompt_followup),
                HumanMessage(content=question),
                AIMessage(content=result_text),
                HumanMessage(content=instruction_text)
            ])
            return followup.content.strip()
    return response.content.strip()

# Example usage
if __name__ == "__main__":
    print("Q1:", query("test", [], "", "I want to find infomation about álslsflfa inside the project"))
    print("Q2:", query("test", [], "", "What is EC2 auto scaling?"))
    print("Q3:", query("test", [], "", "I want to find infomation about permission inside the project"))