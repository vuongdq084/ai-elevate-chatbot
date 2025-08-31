# AI Elevate Chatbot

A multilingual AI chatbot system that provides technical support and documentation assistance with both web and command-line interfaces.

## 🏗️ Project Structure

```
ai-elevate-chatbot/
├── src/                          # Source code
│   ├── main.py                   # Main entry point
│   ├── config/                   # Configuration
│   │   └── settings.py          # App settings
│   ├── core/                     # Core functionality
│   │   ├── chat_engine/         # AI chat processing
│   │   ├── context_manager/     # Document context
│   │   ├── user_manager/        # User management
│   │   └── tts_engine/          # Text-to-speech
│   └── web/                     # Web interface
│       ├── routes.py            # API routes
│       └── static/              # Frontend files
├── data/                         # Data storage
│   ├── documents/               # Project documents
│   ├── audio/                   # Generated audio
│   └── chroma_db/               # Vector database
├── scripts/                      # Utility scripts
├── tests/                        # Test files
├── docs/                         # Documentation
└── requirements.txt              # Dependencies
```

## 🚀 Features

- **Multilingual Support**: Vietnamese and English
- **Dual Interface**: Web UI and Command Line
- **Context Awareness**: Smart document search
- **Audio Generation**: Text-to-speech responses
- **User Persistence**: Chat history management
- **Vector Database**: ChromaDB for context storage

## 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd ai-elevate-chatbot
   ```

2. **Set up a virtual environment (Recommended - Optional)**
   ```bash
   # Create a new virtual environment named venv_test
   python -m venv venv_test
   ```
   - **Activate the virtual environment:**
     - On Windows (cmd):
       ```
       venv_test\Scripts\activate.bat
       ```
     - On Windows (PowerShell):
       ```
       venv_test\Scripts\Activate.ps1
       ```
     - On Mac/Linux:
       ```
       source venv_test/bin/activate
       ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   # Create .env file
   OPENAI_API_KEY=your_api_key
   OPENAI_API_BASE=your_azure_endpoint
   ```

5. **Run the application**
   ```bash
   python src/main.py
   ```

## 🎯 Usage

### Web Interface
```bash
python src/main.py
# Choose option 1
# Open browser to http://localhost:5000
```

### Command Line Interface
```bash
python src/main.py
# Choose option 2
# Follow interactive prompts
```

## 🔧 Configuration

Edit `src/config/settings.py` to modify:
- Server host/port
- Database paths
- Audio settings
- File directories

## 📚 API Endpoints

- `GET /` - Main page
- `POST /history` - Get chat history
- `POST /chat` - Send message and get response
- `GET /audio/<filename>` - Download audio files

## 🗄️ Database

Uses ChromaDB for:
- User chat history
- Document context storage
- Vector embeddings

## 🎵 Audio Generation

- Generates WAV files for responses
- Supports multiple languages
- Configurable output quality

## 🧪 Testing

```bash
# Run tests
python -m pytest tests/
```

## 📝 Development

### Adding New Features
1. Create module in appropriate `src/core/` directory
2. Add configuration in `src/config/settings.py`
3. Update routes in `src/web/routes.py` if needed
4. Test both CLI and web interfaces

### Code Style
- Follow Python PEP 8
- Use descriptive function names
- Add docstrings for all functions
- Keep modules focused and single-purpose

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

For issues and questions:
- Check the documentation
- Review existing issues
- Create a new issue with detailed description
