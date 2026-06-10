import asyncio
import os
import aiohttp
from flask import Flask, render_template

app = Flask(__name__)

async def check_speed(session, url):
    try:
        start = asyncio.get_event_loop().time()
        async with session.get(url, timeout=5) as response:
            if response.status == 200:
                return asyncio.get_event_loop().time() - start
    except Exception:
        pass
    return float('inf')

async def get_sorted_streams():
    urls = []
    if os.path.exists("live.txt"):
        with open("live.txt", "r", encoding="utf-8") as f:
            urls.extend(f.readlines())
    if os.path.exists("local.txt"):
        with open("local.txt", "r", encoding="utf-8") as f:
            urls.extend(f.readlines())
            
    valid_urls = [url.strip() for url in urls if "," in url]
    
    async with aiohttp.ClientSession() as session:
        tasks = [check_speed(session, url.split(",")[1]) for url in valid_urls]
        results = await asyncio.gather(*tasks)
        
    scored_urls = list(zip(valid_urls, results))
    scored_urls.sort(key=lambda x: x[1])
    
    sorted_content = "\n".join([item[0] for item in scored_urls])
    return sorted_content

@app.route("/")
def index():
    content = asyncio.run(get_sorted_streams())
    return render_template("index.html", content=content)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=4545)
