# Python Learning Chatbot

A RAG (Retrieval-Augmented Generation) chatbot that answers Python questions
using a custom knowledge base. Built as a learning project to practice
GitHub Actions CI/CD and AI application development.

## What It Does

Ask the chatbot about Python concepts, and it answers **based on your own notes**
— not from the model's general training. This reduces hallucinations and keeps
answers grounded in the material you provide.

Example:
```
Ask about Python (or type 'exit'): What is a list comprehension?

Python list comprehensions provide a short, readable way to build a list
in a single expression...
```

## How It Works

```
User question
     ↓
retrieve() searches documents/
     ↓
Finds the most relevant lines
     ↓
Sends question + context to Groq API
     ↓
Model answers grounded in the documents
```

## Tech Stack

- **Python 3.12**
- **OpenAI SDK** (pointing at Groq's OpenAI-compatible endpoint)
- **Groq API** — model: `openai/gpt-oss-120b`
- **GitHub Actions** — CI pipeline runs tests on every push
- **pytest** — test framework

## Project Structure

```
python-ci-demo/
├── .github/workflows/ci.yml   # CI pipeline
├── documents/
│   └── python_notes.txt        # Knowledge base
├── chatbot.py                  # RAG chatbot
├── requirements.txt
├── test_sample.py
└── README.md
```

## Setup

1. Clone the repo:
   ```bash
   git clone https://github.com/snappool/python-ci-demo.git
   cd python-ci-demo
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Get a free Groq API key from https://console.groq.com

4. Set it as an environment variable:
   ```bash
   export GROQ_API_KEY=gsk_your_key_here
   ```

5. Run the chatbot:
   ```bash
   python chatbot.py
   ```

## CI Pipeline

Every push to `main` triggers GitHub Actions to:
1. Spin up a fresh Ubuntu VM
2. Install Python 3.10
3. Install dependencies from `requirements.txt`
4. Run tests with `pytest`

A ✅ or ❌ appears next to each commit.

## What I Learned

- Building a CI/CD pipeline with GitHub Actions
- Writing workflows in YAML
- Debugging failing CI runs
- Implementing a basic RAG pipeline
- Working with LLM APIs (Groq, OpenAI SDK)
- Managing secrets with environment variables

## License

MIT
