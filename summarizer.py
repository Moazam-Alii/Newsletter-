from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def summarize_post(text):
    prompt = f"""
You are an expert newsletter curator.

Your job is to generate:
1. A catchy, engaging **heading** (3–6 words) suitable for newsletters (bold text).
2. A short, punchy **summary** in 1–2 sentences. Avoid describing the post, author, or platform.

Instructions:
- Heading should be bold and appear on the first line.
- Summary should start from a new line.
- Use a confident, insightful tone.
- Do not mention LinkedIn, posts, or authors.
- Avoid generic phrases like "This post discusses..."

Post Content:
{text}
"""
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5
    )
    
    output = response.choices[0].message.content.strip()

    # Split heading and summary
    lines = output.split('\n')
    heading = next((line.strip() for line in lines if line.strip().startswith("**")), "No Heading")
    summary = "\n".join([line.strip() for line in lines if not line.strip().startswith("**")])

    print(f"{heading}\n{summary}")
    return heading, summary
