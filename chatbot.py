import os
from openai import OpenAI

# Read documents in the knowledge base
def load_docs(folder="documents"):
    texts = []
    for f in os.listdir(folder):
        with open(os.path.join(folder, f), "r", encoding="utf-8") as file:
            texts.append(file.read())
    return "\n".join(texts)

# Simple keyword retrieval (can be replaced with vector search later)
def retrieve(question, knowledge, lines=5):
    lines_list = knowledge.split("\n")
    # Very crude matching, just to demonstrate the concept
    scored = [(line, sum(word in line for word in question.split())) for line in lines_list]
    scored.sort(key=lambda x: x[1], reverse=True)
    return "\n".join([l for l, s in scored[:lines]])

# Main flow
knowledge = load_docs()
client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=os.environ["GROQ_API_KEY"]
)

while True:
    question = input("\nAsk about Python (or type 'exit'): ")
    if question.lower() in ("exit", "quit"):
        print("Goodbye!")
        break

    context = retrieve(question, knowledge)

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {"role": "system", "content": f"Answer questions based only on the following content:\n{context}"},
            {"role": "user", "content": question}
        ]
    )
    print("\n" + response.choices[0].message.content)

