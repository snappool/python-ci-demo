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

def retrieve(question, docs, lines=25):
    """Search across all files, return top matching lines with their source."""
    stopwords = {"what", "how", "the", "a", "an", "of", "to", "in",
                 "on", "for", "with", "do", "i", "you", "me", "my"}

    raw = question.lower().split()
    words = []
    special = {"==", "!=", "<", ">", "<=", ">=", "is", "and", "or", "not"}

    for w in raw:
        raw_clean = w.rstrip("?").rstrip(".")
        if raw_clean in special:
            words.append(raw_clean)
            continue
        stripped = w.strip(string.punctuation)
        if stripped and stripped not in stopwords:
            words.append(stripped)

    if not words:
        words = raw

    results = []
    for filename, content in docs.items():
        for line in content.split("\n"):
            if not line.strip():
                continue
            line_lower = line.lower()
            score = 0
            matched_words = set()
            for word in words:
                if word in line_lower:
                    matched_words.add(word)
                    if word in special:
                        score += 3
                    else:
                        score += 1
            if len(matched_words) >= 2:
                score += len(matched_words) * 5
            if score > 0:
                results.append((score, filename, line))

    results.sort(key=lambda x: x[0], reverse=True)
    top = results[:lines]

    if not top:
        return "No relevant content found in the knowledge base."

    return "\n".join(f"[{fname}] {line}" for _, fname, line in top)

docs = load_docs()

client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=os.environ["GROQ_API_KEY"]
)

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
