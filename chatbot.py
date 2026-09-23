import os
import string
from dotenv import load_dotenv
load_dotenv()
from openai import OpenAI

def load_docs(folder="documents"):
    """Return a dict: {filename: content}"""
    docs = {}
    for f in os.listdir(folder):
        if f.endswith(".txt"):
            with open(os.path.join(folder, f), "r", encoding="utf-8") as file:
                docs[f] = file.read()
    return docs

def retrieve(question, docs, lines=15):
    """Search across all files, return top matching lines with their source."""
    stopwords = {"what", "is", "the", "a", "an", "how", "do", "i",
                 "difference", "between", "and", "or", "to", "of",
                 "in", "on", "for", "with", "can", "you", "me", "my"}

    # Strip punctuation from each word
    words = [
        w.strip(string.punctuation)
        for w in question.lower().split()
    ]
    words = [w for w in words if w not in stopwords and len(w) > 2]

    if not words:
        return "No relevant content found in the knowledge base."

    results = []
    for filename, content in docs.items():
        for line in content.split("\n"):
            if not line.strip():
                continue
            line_lower = line.lower()
            unique_matches = sum(1 for word in words if word in line_lower)
            if unique_matches > 0:
                results.append((unique_matches, filename, line))

    results.sort(key=lambda x: x[0], reverse=True)
    top = results[:lines]

    if not top:
        return "No relevant content found in the knowledge base."

    return "\n".join(f"[{fname}] {line}" for _, fname, line in top)

# Load knowledge base
docs = load_docs()

# Set up Groq client
client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=os.environ["GROQ_API_KEY"]
)

# Interactive loop
while True:
    question = input("\nAsk about Python (or type 'exit'): ").strip()
    if not question:
        continue
    if question.lower() in ("exit", "quit"):
        print("Goodbye!")
        break

    context = retrieve(question, docs)

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {"role": "system", "content": f"Answer the question using ONLY the following content from a Python knowledge base. If the answer isn't there, say so.\n\n{context}"},
            {"role": "user", "content": question}
        ]
    )
    print("\n" + response.choices[0].message.content)
