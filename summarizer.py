from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def summarize_post(text):
    prompt = f"""
You are an expert newsletter curator. 
1:A catchy, engaging **heading** (3–6 words) suitable for newsletters The heading should be in bold and above the summary.
2:Your goal is to extract short, punchy, direct summaries from LinkedIn posts for a B2B tech newsletter.

Instructions:
The heading should be in bold and above the summary.
The summray should start from the new line
Summarize the core idea in 1–2 short sentences.

Make it concise, impactful, and reader-friendly.

Use a tone that's insightful and confident, not explanatory.

Do not describe the LinkedIn post or the author.

Do not mention LinkedIn, the post, or interactions.

Avoid generic phrasing like "The post explains..."

Focus on the core insight or myth-busting message.
Post Content:
{text}
"""
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5
    )
    return response.choices[0].message.content.strip()
