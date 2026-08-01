import os
from groq import Groq
from dotenv import load_dotenv
load_dotenv()
def build_prompt(question, context_chunks):
    context = ""

    for i, chunk in enumerate(context_chunks):
        context += f"Source {i + 1}:\n"
        context += chunk["text"] + "\n\n"

    prompt = f"""
Use only the context below to answer the question.
If the answer is not in the context, say you could not find it. Be Honest.

Context:
{context}

Question:
{question}

Answer:
"""
    return prompt




def generate_answer(question, context_chunks):
    api_key = os.getenv("GROQ_API_KEY")

    client = Groq(api_key=api_key)
    prompt = build_prompt(question, context_chunks)
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )
    return response.choices[0].message.content