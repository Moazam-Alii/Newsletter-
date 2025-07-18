# scraper.py
from playwright.async_api import async_playwright
from urllib.parse import urljoin

async def extract_post_images(page, base_url):
    image_urls = []
    for _ in range(3):
        await page.mouse.wheel(0, 500)
        await page.wait_for_timeout(1000)

    images = await page.locator("article img").all()
    for img in images:
        src = await img.get_attribute("src") or ""
        alt = (await img.get_attribute("alt") or "").lower()
        class_name = (await img.get_attribute("class") or "").lower()
        keywords = ["profile", "avatar", "banner", "emoji", "icon", "logo"]
        if not src or src.startswith("data:image"):
            continue
        if any(k in src.lower() for k in keywords) or any(k in alt for k in keywords) or any(k in class_name for k in keywords):
            continue
        if "media.licdn.com" in src and src not in image_urls:
            image_urls.append(urljoin(base_url, src))

    picture_sources = await page.locator("article picture source").all()
    for source in picture_sources:
        srcset = await source.get_attribute("srcset") or ""
        for src_part in srcset.split(","):
            url = src_part.strip().split(" ")[0]
            if url and "media.licdn.com" in url and url not in image_urls:
                if not any(k in url.lower() for k in ["profile", "avatar", "banner", "emoji", "icon", "logo"]):
                    image_urls.append(urljoin(base_url, url))

    return image_urls

async def scrape_post_content(url):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True, args=["--disable-gpu", "--no-sandbox"])
        page = await browser.new_page()
        await page.goto(url, timeout=60000)

        # Try to get post content from article
        try:
            await page.wait_for_selector("article", timeout=15000)
            content = await page.inner_text("article")
        except:
            print(f"[WARN] 'article' not found for {url}. Falling back to <body>.")
            content = await page.inner_text("body")

        # Scroll to load more
        prev_height = None
        for _ in range(5):
            curr_height = await page.evaluate("document.body.scrollHeight")
            if prev_height == curr_height:
                break
            prev_height = curr_height
            await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            await page.wait_for_timeout(1500)

        # Extract image URLs
        image_urls = await extract_post_images(page, url)
        await browser.close()
        return content, image_urls
