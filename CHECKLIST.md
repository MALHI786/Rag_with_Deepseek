📋 RAG Setup Checklist
=====================

Before running the application, complete these steps:

## Prerequisites

□ Python 3.8+ installed
□ Virtual environment activated (`.venv\Scripts\Activate.ps1`)
□ All packages installed (already done ✓)

## Ollama Setup

□ Download and install Ollama from https://ollama.ai/
□ Start Ollama server: `ollama serve`
□ Pull DeepSeek R1 model: `ollama pull deepseek-r1:1.5b`
□ Verify Ollama is running: `ollama list`

## Groq API Setup

□ Sign up at https://console.groq.com/
□ Generate API key from the dashboard
□ Copy the API key (starts with `gsk_`)

## Environment Configuration

□ Open `.env` file (already created ✓)
□ Replace `your_groq_api_key_here` with your actual Groq API key
□ Save the file

## Test Run

□ Ensure Ollama is running (`ollama serve` in a separate terminal)
□ Activate virtual environment: `.\.venv\Scripts\Activate.ps1`
□ Run: `streamlit run frontend.py`
□ Browser opens automatically at http://localhost:8501

## First Use

□ Upload a PDF file (max 100MB)
□ Click "🚀 Process PDF" button
□ Wait for processing to complete (~30-60 seconds)
□ Start asking questions!

## Troubleshooting

If something doesn't work:

1. Check Ollama is running: `curl http://localhost:11434`
2. Verify API key in `.env` file
3. Check errors in terminal
4. See QUICKSTART.md for detailed troubleshooting

## Ready to Go! 🎉

Once all checkboxes are ticked, you're ready to use your RAG chatbot!

Run: `streamlit run frontend.py`
