import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_heading_from_summary(summary: str) -> str:
    prompt = (
        "Generate a short, catchy 3 to 5 word heading for this LinkedIn post summary:\n"
        f"Summary: {summary}\n"
        "Heading:"
    )

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an expert at writing short, engaging newsletter headings."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=10,
            temperature=0.7,
        )

        heading = response.choices[0].message['content'].strip()
        return heading
    except Exception as e:
        print("❌ Error generating heading:", e)
        return "Post Summary"
