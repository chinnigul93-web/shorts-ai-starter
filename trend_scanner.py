import json
import os
import re
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone

# Google Trends RSS. Change GEO to US, IN, GB, etc. if you want another market.
GEO = os.getenv("TREND_GEO", "UZ")
FEED_URL = f"https://trends.google.com/trending/rss?geo={GEO}"
OUT_DIR = "output"
os.makedirs(OUT_DIR, exist_ok=True)

def clean(text):
    return re.sub(r"\s+", " ", (text or "")).strip()

def main():
    request = urllib.request.Request(
        FEED_URL,
        headers={"User-Agent": "Mozilla/5.0 (compatible; ShortsTrendScanner/1.0)"}
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        xml_data = response.read()

    root = ET.fromstring(xml_data)
    items = []
    for item in root.findall(".//item"):
        title = clean(item.findtext("title"))
        traffic = clean(item.findtext("ht:approx_traffic", default="", namespaces={
            "ht": "https://trends.google.com/trending/rss"
        }))
        pub_date = clean(item.findtext("pubDate"))
        news = []
        for node in item.findall("ht:news_item", {"ht": "https://trends.google.com/trending/rss"}):
            news_title = clean(node.findtext("ht:news_item_title", default="", namespaces={
                "ht": "https://trends.google.com/trending/rss"
            }))
            news_source = clean(node.findtext("ht:news_item_source", default="", namespaces={
                "ht": "https://trends.google.com/trending/rss"
            }))
            if news_title:
                news.append({"title": news_title, "source": news_source})
        if title:
            items.append({
                "topic": title,
                "approx_traffic": traffic,
                "published": pub_date,
                "related_news": news[:3],
                "status": "needs_editorial_check"
            })

    payload = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "geo": GEO,
        "source": FEED_URL,
        "count": len(items),
        "topics": items
    }
    json_path = os.path.join(OUT_DIR, "trends.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

    md_path = os.path.join(OUT_DIR, "trends.md")
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(f"# Google Trends — {GEO}\n\n")
        f.write(f"Generated: {payload['generated_at_utc']}\n\n")
        if not items:
            f.write("No topics were returned. Check the RSS feed or change TREND_GEO.\n")
        for index, topic in enumerate(items, 1):
            f.write(f"## {index}. {topic['topic']}\n")
            if topic["approx_traffic"]:
                f.write(f"- Approx. traffic: {topic['approx_traffic']}\n")
            if topic["published"]:
                f.write(f"- Published: {topic['published']}\n")
            for story in topic["related_news"]:
                source = f" ({story['source']})" if story["source"] else ""
                f.write(f"- Related news: {story['title']}{source}\n")
            f.write("- Review: confirm relevance, accuracy, and suitability before making a video.\n\n")

    print(f"Saved {len(items)} topics to {json_path} and {md_path}")

if __name__ == "__main__":
    main()
