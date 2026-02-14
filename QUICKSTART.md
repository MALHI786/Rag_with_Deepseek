# 🚀 Quick Start Guide

## Before You Begin

Make sure you have:
1. ✅ Ollama installed and running
2. ✅ DeepSeek R1 model pulled in Ollama
3. ✅ Groq API key ready

## Step-by-Step Setup

### 1. Check Ollama is Running

Open a new terminal and run:

```powershell
ollama serve
```

Leave this terminal open. Ollama needs to be running in the background.

### 2. Pull DeepSeek R1 Model

In another terminal:

```powershell
ollama pull deepseek-r1:1.5b
```

Wait for the download to complete (~1GB).

### 3. Get Your Groq API Key

1. Go to https://console.groq.com/
2. Sign up or log in
3. Go to API Keys section
4. Create a new API key
5. Copy the API key

### 4. Configure Environment

Open `.env` file in your project folder:

```powershell
notepad .env
```

Replace `your_groq_api_key_here` with your actual API key:

```bash
GROQ_API_KEY=gsk_YOUR_ACTUAL_API_KEY_HERE
```

Save and close the file.

### 5. Activate Virtual Environment

```powershell
.\.venv\Scripts\Activate.ps1
```

You should see `(.venv)` in your terminal prompt.

### 6. Run the Application

```powershell
streamlit run frontend.py
```

The app will open in your browser automatically!

## Using the App

### First Time:

1. **Upload PDF**: Click "Browse files" in the sidebar
2. **Process PDF**: Click "🚀 Process PDF" button (wait ~30-60 seconds)
3. **Ask Questions**: Type in the chat input and press Enter

### Tips:

- ⏱️ First question may take 10-20 seconds (model initialization)
- 📄 PDFs up to 100MB are supported
- 🔄 You can clear chat or upload a new PDF anytime
- ⚡ Subsequent questions are faster

## Troubleshooting

### "Could not connect to Ollama"

**Problem**: Ollama is not running

**Solution**: 
```powershell
ollama serve
```

### "GROQ_API_KEY not found"

**Problem**: API key not configured

**Solution**: 
1. Edit `.env` file
2. Add your actual Groq API key
3. Restart the application

### "Model not found"

**Problem**: DeepSeek R1 model not downloaded

**Solution**:
```powershell
ollama pull deepseek-r1:1.5b
```

### PDF Processing Too Slow

**Solutions**:
- Use smaller PDFs (< 10MB recommended)
- Use a faster model: `ollama pull deepseek-r1:1.5b`
- Close other applications

### Out of Memory

**Solutions**:
- Use smaller PDFs
- Restart Ollama
- Close other applications

## Example Questions

Once your PDF is processed, try:

- "What is the main topic?"
- "Summarize the document in 3 sentences"
- "What does it say about [topic]?"
- "Explain [concept] from the document"
- "List the key findings"

## Model Options

### Ollama Models (for embeddings):

```powershell
# Fast & light (recommended)
ollama pull deepseek-r1:1.5b

# More accurate but slower
ollama pull deepseek-r1:7b
```

Update in `.env`:
```bash
OLLAMA_MODEL=deepseek-r1:1.5b
```

### Groq Models (for answers):

Available in `.env`:
- `deepseek-r1-distill-llama-70b` - Best quality (default)
- `deepseek-r1-distill-llama-8b` - Faster, smaller

## Need Help?

Check the full [README.md](README.md) for detailed documentation.

---

**Happy chatting! 🎉**
