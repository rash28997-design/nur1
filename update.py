import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime
from html import escape, unescape

# BBC বাংলা RSS
RSS_URL = "https://feeds.bbci.co.uk/bengali/rss.xml"


def fetch_news():
    try:
        request = urllib.request.Request(
            RSS_URL,
            headers={
                "User-Agent": "Mozilla/5.0"
            }
        )

        with urllib.request.urlopen(request, timeout=20) as response:
            data = response.read()

        root = ET.fromstring(data)

        news_html = ""
        count = 0

        for item in root.findall("./channel/item"):

            if count >= 6:
                break

            title = item.findtext("title", "").strip()
            link = item.findtext("link", "").strip()
            description = item.findtext("description", "").strip()

            if not title or not link:
                continue

            title = escape(unescape(title))
            description = escape(unescape(description))
            link = escape(link, quote=True)

            news_html += f"""
<div class="news-card">
    <h3>
        <a href="{link}" target="_blank" rel="noopener noreferrer">
            {title}
        </a>
    </h3>
    <p>{description}</p>
</div>
"""

            count += 1

        if news_html:
            return news_html

        return """
<div class="news-card">
    <h3>কোনো খবর পাওয়া যায়নি</h3>
</div>
"""

    except Exception as e:
        print("NEWS ERROR:", e)

        return """
<div class="news-card">
    <h3>খবর লোড করতে সমস্যা হয়েছে</h3>
    <p>কিছুক্ষণ পরে আবার চেষ্টা করুন।</p>
</div>
"""


def update_website():

    try:
        with open("index.html", "r", encoding="utf-8") as file:
            html_content = file.read()

    except FileNotFoundError:
        print("ERROR: index.html পাওয়া যায়নি!")
        return

    start_marker = "<!-- START_NEWS -->"
    end_marker = "<!-- END_NEWS -->"

    if start_marker not in html_content:
        print("ERROR: START_NEWS পাওয়া যায়নি!")
        return

    if end_marker not in html_content:
        print("ERROR: END_NEWS পাওয়া যায়নি!")
        return

    # নতুন বাংলা খবর
    news = fetch_news()

    before = html_content.split(start_marker, 1)[0]
    after = html_content.split(end_marker, 1)[1]

    updated = (
        before
        + start_marker
        + "\n"
        + news
        + "\n"
        + end_marker
        + after
    )

    # আপডেটের সময়
    current_time = datetime.now().strftime("%d-%m-%Y %I:%M %p")

    time_start = '<span id="last-updated">'
    time_end = "</span>"

    if time_start in updated:

        first_part = updated.split(time_start, 1)[0]
        remaining = updated.split(time_start, 1)[1]

        if time_end in remaining:

            last_part = remaining.split(time_end, 1)[1]

            updated = (
                first_part
                + time_start
                + current_time
                + time_end
                + last_part
            )

    # index.html আপডেট
    with open("index.html", "w", encoding="utf-8") as file:
        file.write(updated)

    print("SUCCESS: বাংলা খবর আপডেট হয়েছে!")
    print("সময়:", current_time)


if __name__ == "__main__":
    update_website()
