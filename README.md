# AI Elevate Chatbot

An intelligent chatbot system with Azure OpenAI integration and FAQ database support.

## Features

- **Module 1 (main.py)**: Main program flow with user interaction
- **Module 2 (user_manager/)**: User management with chat history persistence
- **Module 3 (context_manager/)**: Context management with FAQ database integration
- **Module 4 (chat_engine/)**: Query processing with Azure OpenAI API
- **Azure OpenAI Integration**: Uses Azure OpenAI GPT-4o-mini for intelligent responses
- **FAQ Database**: Built-in AWS Auto Scaling FAQ knowledge base
- **Multilingual Support**: Supports both English and Vietnamese

## Setup

### 1. Install Dependencies

Run the setup script:

```bash
setup.bat
```

Or manually install:

```bash
pip install openai==1.35.5
```

### 2. Azure OpenAI Configuration

The system is pre-configured with Azure OpenAI settings in `config/openai_config.py`:

- Endpoint: https://aiportalapi.stu-platform.live/jpe
- Model: GPT-4o-mini
- API Version: 2024-07-01-preview

### 3. FAQ Database

The system includes a comprehensive AWS Auto Scaling FAQ database in `questions_and_answers.txt`.

## Usage

### Run the Main Application

```bash
python main.py
```

### Run the Demo

```bash
python demo.py
```

## System Architecture

```
ai-elevate-chatbot/
├── main.py                    # Module 1: Main program flow
├── user_manager/
│   ├── __init__.py
│   └── user.py               # Module 2: User management
├── context_manager/
│   ├── __init__.py
│   └── context.py            # Module 3: Context management
├── chat_engine/
│   ├── __init__.py
│   └── query.py              # Module 4: Query processing
├── config/
│   ├── __init__.py
│   └── openai_config.py      # Azure OpenAI configuration
├── shared/
│   ├── __init__.py
│   └── types.py              # Shared data types
├── questions_and_answers.txt  # FAQ database
├── requirements.txt
├── setup.bat
├── demo.py
└── README.md
```

## Main Program Flow

1. **User Authentication**: Request user to enter username
2. **Load User History**: Call Module 2.LoadUser to get chat history
3. **Question Input**: Request user to enter question
4. **Context Loading**: Call Module 3.LoadContext to get relevant context
5. **Answer Generation**: Call Module 4.Query to generate response using Azure OpenAI
6. **Display Answer**: Show the AI response to user
7. **Save Chat**: Call Module 2.SaveChat to save the conversation

## Example Usage

```
=== AI Elevate Chatbot ===
Welcome to the AI Chatbot System with Azure OpenAI!

Enter your user name: john_doe

--- Loading User History for 'john_doe' ---
✓ New user detected. Starting fresh conversation.

--- Chat Session ---
Enter your question (or 'quit' to exit): What is Amazon EC2 Auto Scaling?

🔍 Searching for relevant context...
✓ Relevant context found!
🤖 Generating response...

--- AI Response ---
🤖 Answer: Amazon EC2 Auto Scaling is a fully managed service designed to launch or terminate Amazon EC2 instances automatically to help ensure you have the correct number of Amazon EC2 instances available to handle the load for your application...

💾 Saving conversation...
Chat saved for user john_doe
```

## FAQ Categories

The system includes FAQ entries covering:

- Amazon EC2 Auto Scaling basics
- Auto Scaling Groups (ASG)
- Scaling policies (target tracking, predictive scaling)
- Fleet management
- Launch configurations
- AWS Auto Scaling vs EC2 Auto Scaling

## API Integration

The system uses Azure OpenAI with:

- **Model**: GPT-4o-mini
- **Temperature**: 0.3 (for consistent responses)
- **Max Tokens**: 500
- **Language Support**: Auto-detection of English/Vietnamese

## Error Handling

- Graceful fallback to rule-based responses if OpenAI API is unavailable
- File I/O error handling for user data and FAQ loading
- Network error handling for API calls

## Development

### Adding New FAQ Entries

Add questions and answers to `questions_and_answers.txt` in the format:

```
Q: Your question here?
Your answer here.

Q: Next question?
Next answer here.
```

### Extending Context Database

Modify `context_manager/context.py` to add new context sources or integrate with vector databases.

### Customizing OpenAI Behavior

Update the system prompt in `chat_engine/query.py` or modify `config/openai_config.py` settings.
