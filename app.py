from flask import Flask, render_template, request
from scraper import scrape_post_content
from cleaner import clean_post_text
from summarizer import summarize_post
from heading import generate_heading_from_summary

from dotenv import load_dotenv
import asyncio
import os

load_dotenv()

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')  # if you're using 'start.html', update this name accordingly

@app.route('/results', methods=['POST'])
def scrape():

    post_urls = request.form.getlist("post_urls[]")  # This must match name="post_urls[]" in your HTML

    print("RAW URLS >>>", post_urls)

    post_urls = post_urls[:20]

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

            heading = generate_heading_from_summary(summary)

            results.append({
                'heading': heading,
                'summary': summary,
                'image': image_urls[0] if image_urls else None,
                'url': url
            })
        except Exception as e:
            print(f"❌ Error scraping {url}: {e}")
            continue
    return results


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
