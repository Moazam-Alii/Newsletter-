from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def clean_post_text(text):
    prompt = f"""
You are a smart content cleaner. Given the following LinkedIn post content, extract only the useful text that seems like the main body of the post and try not to add the comments of the post also dont add the bio of profiles. Ignore these keywords and metadata: followers, reactions, comments, reply, student at, like, 1h, 2h, 3h, minutes ago, contact us.
But dont change the body of the post content use exact same words same emojis(if any).
--- Raw Text ---
{text}
"""
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )
    return response.choices[0].message.content.strip()
