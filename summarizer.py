from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def summarize_post(text):
    prompt = f"""
Write a 2–3 line summary of the following LinkedIn post content. Make it informative, keep the tone professional, and avoid repeating the whole post.

Post Content:
{text}
"""
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5
    )
    return response.choices[0].message.content.strip()
