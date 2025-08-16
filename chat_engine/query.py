def query(user_id, history, context, question):
<<<<<<< Updated upstream
    # Dummy query logic
    return f"Based on context '{context}', the answer to your question is: [dummy answer]."
=======
    messages = [
        {"role": "system", "content": context},
        {"role": "user", "content": question}
    ]

    function_definitions = [
        {
            "name": "search_document",
            # "description": "Tìm document phù hợp với keyword từ câu hỏi người dùng",
            "description": "Find the relevant document based on the keyword from the user question, and return the answer in user's language",
            "parameters": {
                "type": "object",
                "properties": {
                    "keyword": {
                        "type": "string",
                        # "description": "Từ khóa cần tìm trong document, ví dụ: permission, hệ thống, guideline"
                        "description": "Read the user question and extract the keyword to search for the relevant document, e.g., permission, system, guideline"
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
        with open('system.txt','r',encoding = 'utf-8') as f:
            system_prompt = f.read()
        
        followup_messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": question},
            {"role": "assistant", "content": f"Với {question}, câu trả lời là: {result}"}
            # {"role": "user", "content": "Hãy phản hồi lại người dùng bằng một câu trả lời thân thiện, nếu tìm thấy document phải cho thêm link document vào câu trả lời. Nếu không tìm thấy hỏi thêm thông tin"}
        ]
        response = get_response(followup_messages)
        answer = response.choices[0].message.content.strip()
    else:
        answer = response.choices[0].message.content.strip()

    #print("Answer:\n")
    #print(answer)
        
    #return f"Based on context '{context}', the answer to your question is: {answer}."
    return answer
>>>>>>> Stashed changes
