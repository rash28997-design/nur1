import requests
from bs4 import BeautifulSoup
from datetime import datetime

def fetch_news():
    try:
        # বিবিসি বাংলা থেকে খবর স্ক্র্যাপ করা হচ্ছে
        url = "https://bbc.com"
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        articles = soup.find_all('h3')
        news_html = ""
        count = 0
        
        for article in articles:
            title = article.get_text().strip()
            link_tag = article.find('a')
            
            if link_tag and title and count < 6: # সর্বোচ্চ ৬টি তাজা খবর নেবে
                link = link_tag['href']
                if not link.startswith('http'):
                    link = "https://bbc.com" + link
                    
                news_html += f'''
            <div class="news-card">
                <h3><a href="{link}" target="_blank">{title}</a></h3>
                <p>বিস্তারিত পড়তে শিরোনামের ওপর ক্লিক করুন।</p>
            </div>\n'''
                count += 1
                
        return news_html if news_html else "<!-- NO_NEWS -->"
    except Exception as e:
        return "<!-- ERROR_NEWS -->"

def update_website():
    current_time = datetime.now().strftime("%d-%m-%Y %I:%M %p")
    new_news = fetch_news()
    
    with open("index.html", "r", encoding="utf-8") as file:
        html_content = file.read()
        
    # নিখুঁতভাবে খবরের অংশ পরিবর্তন
    start_marker = "<!-- START_NEWS -->"
    end_marker = "<!-- END_NEWS -->"
    
    if start_marker in html_content and end_marker in html_content:
        before_news = html_content.split(start_marker)[0]
        after_news = html_content.split(end_marker)[1]
        updated_content = before_news + start_marker + "\n" + new_news + "            " + end_marker + after_news
    else:
        updated_content = html_content
    
    # নিখুঁতভাবে টাইমস্ট্যাম্প আপডেট
    time_start = '<span id="last-updated">'
    time_end = '</span>'
    
    if time_start in updated_content and time_end in updated_content:
        time_before = updated_content.split(time_start)[0]
        time_after = updated_content.split(time_end)[1]
        final_content = time_before + time_start + current_time + time_end + time_after
    else:
        final_content = updated_content
    
    with open("index.html", "w", encoding="utf-8") as file:
        file.write(final_content)

if __name__ == "__main__":
    update_website()
