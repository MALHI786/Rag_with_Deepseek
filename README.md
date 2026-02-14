# 📚 RAG Chatbot with DeepSeek

A fully-functional RAG (Retrieval Augmented Generation) application that lets you chat with your PDF documents using DeepSeek R1 AI models.

## 🎯 Features

- ✨ **Modern Streamlit UI** - Clean, professional interface
- 📄 **PDF Upload & Processing** - Upload PDFs up to 100MB
- 🧠 **DeepSeek R1 Embeddings** - Powered by Ollama for local embeddings
- 🚀 **DeepSeek R1 LLM** - Via Groq API for fast inference
- 🔍 **FAISS Vector Store** - Efficient similarity search
- 💬 **Interactive Chat** - Ask questions about your documents
- 📊 **Real-time Status** - Visual feedback throughout the process

## 🏗️ Architecture

### Phase 1: Streamlit UI
- PDF upload functionality
- Chat interface with message history
- Status tracking and error handling

### Phase 2: Vector Database
- PDF loading with PDFPlumber
- Text chunking (RecursiveCharacterTextSplitter)
- DeepSeek R1 embeddings via Ollama
- FAISS vector store indexing

### Phase 3: RAG Pipeline
- DeepSeek R1 LLM via Groq API
- Document retrieval from FAISS
- Context-aware answer generation

### Phase 4: Integration
- Complete end-to-end pipeline
- Error handling and user feedback
- Session state management

## 📋 Prerequisites

1. **Python 3.8+** installed
2. **Ollama** installed and running ([Download Ollama](https://ollama.ai/))
3. **Groq API Key** ([Get free API key](https://console.groq.com/))

## 🚀 Installation

### 1. Install Ollama (Docker or Native) and Pull DeepSeek R1

#### Option A: Using Docker (Recommended)

```powershell
# Check if Ollama container is running
docker ps

# If not running, start Ollama container
docker run -d --name ollama `
  -p 11434:11434 `
  -v ${env:USERPROFILE}\.ollama:/root/.ollama `
  --restart unless-stopped `
  ollama/ollama:latest

# For GPU support (if available)
docker run -d --name ollama `
  --gpus all `
  -p 11434:11434 `
  -v ${env:USERPROFILE}\.ollama:/root/.ollama `
  --restart unless-stopped `
  ollama/ollama:latest

# Pull DeepSeek R1 model inside Docker container
docker exec -it ollama ollama pull deepseek-r1:1.5b

# Verify the model
docker exec -it ollama ollama list

# Test the model (optional)
docker exec -it ollama ollama run deepseek-r1:1.5b "Hello, are you ready?"
```

#### Option B: Native Installation

```powershell
# Download and install Ollama from https://ollama.ai/

# Pull the DeepSeek R1 model (1.5B parameter version)
ollama pull deepseek-r1:1.5b

# Verify Ollama is running
ollama list
```

### 2. Set Up Python Environment

```powershell
# The virtual environment is already created
# Activate it:
.\.venv\Scripts\Activate.ps1

# Install dependencies (already done, but if needed):
pip install -r requirements.txt
```

### 3. Configure Environment Variables

```powershell
# Copy the example env file
Copy-Item .env.example .env

# Edit .env and add your Groq API key
# You can use notepad or any text editor:
notepad .env
```

Update the `.env` file:
```bash
GROQ_API_KEY=your_actual_groq_api_key_here
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=deepseek-r1:1.5b
GROQ_MODEL=llama-3.3-70b-versatile
```

**Note:** If Ollama is running in Docker, it will be accessible at `http://localhost:11434` by default.

## 🎮 Usage

### Start the Application

```powershell
streamlit run frontend.py
```

The app will open automatically in your browser at `http://localhost:8501`

### Using the Chatbot

1. **Upload PDF**: Click the file uploader in the sidebar and select a PDF
2. **Process PDF**: Click the "🚀 Process PDF" button to index the document
3. **Ask Questions**: Type your questions in the chat input
4. **Get Answers**: Receive AI-powered answers based on your document

## 📁 Project Structure

```
Rag With Deepseek/
├── .venv/                  # Virtual environment
├── pdfs/                   # Uploaded PDFs (auto-created)
├── faiss_index/           # FAISS vector store (auto-created)
├── frontend.py            # Streamlit UI application
├── vector_database.py     # Vector DB & PDF processing
├── rag_pipeline.py        # RAG pipeline & LLM integration
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
├── .env                  # Your actual environment variables
└── README.md            # This file
```

## 🔧 Configuration

### Ollama Models

You can use different Ollama models for embeddings:
```bash
ollama pull deepseek-r1:1.5b   # Smaller, faster (recommended)
ollama pull deepseek-r1:7b     # Larger, more accurate
```

Update `OLLAMA_MODEL` in `.env` accordingly.

### Groq Models

Available models on Groq (DeepSeek R1 not available):
- `llama-3.3-70b-versatile` (default, excellent performance)
- `llama-3.1-70b-versatile` (alternative)
- `llama-3.1-8b-instant` (faster, smaller)

Update `GROQ_MODEL` in `.env` to switch models.

**Note:** DeepSeek R1 is not currently available on Groq. We use Llama 3.3 70B for the LLM (text generation) and DeepSeek R1 for embeddings (via Ollama Docker).

### Chunking Parameters

Adjust in the code or add to `.env`:
- `CHUNK_SIZE`: Default 1000 characters
- `CHUNK_OVERLAP`: Default 200 characters
- `RETRIEVAL_K`: Number of chunks to retrieve (default 4)

## 🧪 Testing

### Test Vector Database

```powershell
python vector_database.py
```

### Test RAG Pipeline

```powershell
python rag_pipeline.py
```

### Check Ollama Connection

```powershell
# If using Docker:
docker exec -it ollama ollama list

# Or check the API endpoint
curl http://localhost:11434/api/tags

# Or use Python
python -c "from langchain_ollama import OllamaEmbeddings; print(OllamaEmbeddings(model='deepseek-r1:1.5b'))"
```

## 📚 Dependencies

Key packages:
- `streamlit` - Web interface
- `langchain` - RAG framework
- `langchain-community` - Community integrations
- `langchain-ollama` - Ollama integration
- `langchain-groq` - Groq integration
- `faiss-cpu` - Vector similarity search
- `pdfplumber` - PDF text extraction
- `python-dotenv` - Environment variable management

## 🐛 Troubleshooting

### Ollama Connection Error

```
Error: Could not connect to Ollama
```

**Solution**: Make sure Ollama is running:

```powershell
# If using Docker:
docker ps  # Check if ollama container is running
docker start ollama  # Start if stopped

# If using native installation:
ollama serve
```

### Groq API Key Error

```
Error: GROQ_API_KEY not found
```

**Solution**: 
1. Create `.env` file from `.env.example`
2. Add your Groq API key
3. Restart the application

### PDF Processing Takes Too Long

**Solution**: 
- Use a smaller PDF
- Reduce `CHUNK_SIZE` in vector_database.py
- Use a smaller Ollama model
- **DeepSeek R1 (1536 dims) is faster than Llama 3.2 (3072 dims)**
- Ensure Docker has enough resources allocated
- Use GPU if available (add `--gpus all` to Docker run command)

### Memory Error

**Solution**:
- Close other applications
- Use `faiss-cpu` instead of `faiss-gpu`
- Reduce the number of chunks or retrieval documents
- Allocate more memory to Docker Desktop (Settings > Resources)

## ⚡ Performance Tips

### Using DeepSeek R1 in Docker

DeepSeek R1 (1.5B) offers excellent performance:
- **Embedding dimension:** 1536 (vs 3072 for Llama 3.2) = 50% faster processing
- **Model size:** 1.1GB download
- **Memory footprint:** Lower than larger models
- **Quality:** Optimized for reasoning tasks

### Docker Performance

To maximize performance:

1. **Allocate resources in Docker Desktop:**
   - Go to Settings > Resources
   - Increase CPU (4+ cores recommended)
   - Increase Memory (8GB+ recommended)

2. **Use GPU acceleration (if available):**
   ```powershell
   # Stop existing container
   docker stop ollama
   docker rm ollama
   
   # Start with GPU support
   docker run -d --name ollama --gpus all `
     -p 11434:11434 `
     -v ${env:USERPROFILE}\.ollama:/root/.ollama `
     ollama/ollama:latest
   ```

3. **Monitor Docker container:**
   ```powershell
   # Check resource usage
   docker stats ollama
   
   # View logs
   docker logs ollama -f
   ```

## 🎯 Example Questions

Once you've uploaded a PDF, try asking:
- "What is the main topic of this document?"
- "Summarize the key points"
- "What does it say about [specific topic]?"
- "Can you explain [concept] mentioned in the document?"

## 🔐 Security Notes

- Never commit your `.env` file with real API keys
- The `.gitignore` should exclude `.env`, `pdfs/`, and `faiss_index/`
- API keys are only stored locally

## 📝 License

This project is for educational and personal use.

## 🤝 Contributing

Feel free to fork, modify, and submit pull requests!

## 🙏 Acknowledgments

- **DeepSeek AI** - For the powerful R1 models
- **Groq** - For fast inference API
- **Ollama** - For local model hosting
- **LangChain** - For RAG framework
- **Streamlit** - For the web interface

---

**Built with ❤️ using DeepSeek R1, Groq, Ollama, LangChain & Streamlit**

## Development

To add more features:

1. **Activate the environment:**
   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```

2. **Install new packages:**
   ```powershell
   pip install <package-name>
   pip freeze > requirements.txt
   ```

3. **Run the app:**
   ```powershell
   streamlit run frontend.py
   ```

## Configuration

The app uses Streamlit's default configuration. To customize:

Create `.streamlit/config.toml`:
```toml
[theme]
primaryColor = "#2196f3"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f5f5f5"
textColor = "#262730"
font = "sans serif"

[server]
headless = true
port = 8501
```

## Troubleshooting

**Issue:** Import errors in IDE
- **Solution:** Configure VS Code to use `.venv/Scripts/python.exe` as the interpreter

**Issue:** Port already in use
- **Solution:** Kill the existing Streamlit process or use a different port:
  ```powershell
  streamlit run frontend.py --server.port 8502
  ```

**Issue:** PDF not uploading
- **Solution:** Check file size (must be < 100MB) and ensure it's a valid PDF

## License

This project is for demonstration purposes.

## Author

Built with ❤️ using Streamlit and DeepSeek AI
