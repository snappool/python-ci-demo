# Python Learning Chatbot

A RAG chatbot that answers Python questions using a custom knowledge base.
Built to practice GitHub Actions CI/CD and AI application development.

## What It Does

Answers Python questions **based on your own notes** (in `documents/`),
not the model's general training. This keeps answers grounded and accurate.

## How It Works

```
Question → retrieve() searches documents/ → sends context + question to Groq → answer
```

## Tech Stack

- Python 3.12
- OpenAI SDK (Groq's OpenAI-compatible endpoint)
- Groq API — model: `openai/gpt-oss-120b`
- GitHub Actions + pytest

## Setup

```bash
git clone https://github.com/snappool/python-ci-demo.git
cd python-ci-demo
pip install -r requirements.txt
export GROQ_API_KEY=gsk_your_key_here
python chatbot.py
```

Get a free Groq key at https://console.groq.com

## CI Pipeline

Every push runs GitHub Actions: fresh Ubuntu VM → install Python → install deps → run pytest.

## What I Learned

- GitHub Actions CI/CD
- YAML workflows
- Debugging failing CI runs
- RAG pipeline basics
- LLM APIs (Groq, OpenAI SDK)
- Managing secrets with environment variables

## License

MIT
