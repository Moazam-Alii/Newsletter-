from flask import Flask, render_template, request
from scraper import scrape_post_content
from cleaner import clean_post_text
from summarizer import summarize_post
from dotenv import load_dotenv
import asyncio
import os

load_dotenv()

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/results', methods=['POST'])
def scrape():
    raw_text = request.form.get("post_urls", "")
    post_urls = [line.strip() for line in raw_text.splitlines() if line.strip()][:20]

    print("RAW URLS >>>", post_urls)

    # Run asyncio event loop to process all URLs
    results = asyncio.run(process_all_posts(post_urls))

    print("RESULTS >>>", results)

    return render_template('results.html', posts=results)


async def process_all_posts(post_urls):
    results = []
    for url in post_urls:
        try:
            content, image_urls = await scrape_post_content(url)
            if not content:
                continue

            cleaned = clean_post_text(content)
            summary = summarize_post(cleaned)

            results.append({
                'summary': summary,
                'image': image_urls[0] if image_urls else None,
                'url': url
            })
        except Exception as e:
            print(f"❌ Error scraping {url}: {e}")
            continue
    return results


if __name__ == '__main__':
    app.run(debug=True)
