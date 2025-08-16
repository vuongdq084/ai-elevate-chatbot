from openai import AzureOpenAI
import os
import json
 
os.environ["AZURE_OPENAI_ENDPOINT"] = "https://aiportalapi.stu-platform.live/jpe"
os.environ["AZURE_OPENAI_API_KEY"] = ""
os.environ["AZURE_DEPLOYMENT_NAME"] = "GPT-4o-mini"
 
# Step 1: Init OpenAI client
api_version = "2024-07-01-preview"
client = AzureOpenAI(
  api_version=api_version,
  azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
  api_key=os.getenv("AZURE_OPENAI_API_KEY"),
)

def get_response_with_function(messages, function_definitions):
  response = client.chat.completions.create(
    model=os.getenv("AZURE_DEPLOYMENT_NAME"),
    messages=messages,
    temperature=0.3,
    max_tokens=500,
    functions=function_definitions,
    function_call="auto"
  )

  return response

def get_response(messages):
  response = client.chat.completions.create(
    model=os.getenv("AZURE_DEPLOYMENT_NAME"),
    messages=messages,
    temperature=0.3,
    max_tokens=500
  )

  return response

def search_document(keyword):
    # Dummy search
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
        "architecture": "https://github.com/your-org/qna-system-design"
    }
    return documents.get(keyword.lower(), "Không tìm thấy document phù hợp.")

# Example query triggers function, query("test", "test", "Bạn là chatbot hỗ trợ tra cứu thông tin dự án", "Tôi muốn tìm thông tin về permission trong dự án")
# Example question does not trigger function, query("test", "test", "Bạn là chatbot hỗ trợ tra cứu thông tin dự án", "What is ec2 auto scaling?")
def query(user_id, history, context, question):
    messages = [
        {"role": "system", "content": context},
        {"role": "user", "content": question}
    ]

    function_definitions = [
        {
            "name": "search_document",
            "description": "Tìm document phù hợp với keyword từ câu hỏi người dùng",
            "parameters": {
                "type": "object",
                "properties": {
                    "keyword": {
                        "type": "string",
                        "description": "Từ khóa cần tìm trong document, ví dụ: permission, hệ thống, guideline"
                    }
                },
                "required": ["keyword"]
            }
        }
    ]
    response = get_response_with_function(messages, function_definitions)

    # User prompt matches with function
    if response.choices[0].finish_reason == "function_call":
        func_call = response.choices[0].message.function_call
        print("Function name:", func_call.name)
        print("Arguments:", func_call.arguments)
 
        # Parse arguments và gọi hàm
        arguments = json.loads(func_call.arguments)
        result = search_document(arguments["keyword"])
        print("Tìm thấy document:", result)
 
        # Gửi lại OpenAI để tạo phản hồi cho người dùng
        followup_messages = [
            {"role": "system", "content": "Bạn là trợ lý kỹ thuật hỗ trợ người dùng tìm tài liệu dự án."},
            {"role": "user", "content": question},
            {"role": "assistant", "content": f"Với {question}, câu trả lời là: {result}"},
            {"role": "user", "content": "Hãy phản hồi lại người dùng bằng một câu trả lời thân thiện, nếu tìm thấy document phải cho thêm link document vào câu trả lời. Nếu không tìm thấy hỏi thêm thông tin"}
        ]
        response = get_response(followup_messages)
        answer = response.choices[0].message.content.strip()
    else:
        answer = response.choices[0].message.content.strip()

    #print("Answer:\n")
    #print(answer)
        
    #return f"Based on context '{context}', the answer to your question is: {answer}."
    return answer
