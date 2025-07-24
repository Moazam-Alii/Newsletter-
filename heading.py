from openai import OpenAI
import os
from dotenv import load_dotenv
import re
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_heading_from_summary(summary: str) -> str:
    prompt = (
        "Generate a short, catchy 3 to 5 word heading for this LinkedIn post summary:\n"
        f"Summary: {summary}\n"
        "Heading:"
    )

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an expert at writing short, engaging newsletter headings."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=10,
            temperature=0.7,
        )

        raw_heading = response.choices[0].message.content.strip()
        heading = re.sub(r'^["“”\'`]+|["“”\'`]+$', '', raw_heading)

        return heading
    except Exception as e:
        import traceback
        traceback.print_exc()
        print("❌ Error generating heading:", e)
        return "Post Summaryyy"
