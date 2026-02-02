import feedparser
import requests
import time
import html
import os
from datetime import datetime, timedelta, timezone

# GitHub Secrets에서 값을 가져오거나, 로컬 config.py에서 가져옴
try:
    import config
    TELEGRAM_BOT_TOKEN = getattr(config, 'TELEGRAM_BOT_TOKEN', os.environ.get('TELEGRAM_BOT_TOKEN'))
    TELEGRAM_CHAT_ID = getattr(config, 'TELEGRAM_CHAT_ID', os.environ.get('TELEGRAM_CHAT_ID'))
    SEARCH_QUERY = getattr(config, 'SEARCH_QUERY', '비트코인')
except ImportError:
    TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
    TELEGRAM_CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID')
    SEARCH_QUERY = os.environ.get('SEARCH_QUERY', '비트코인')

def send_telegram_message(text):
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("에러: 텔레그램 토큰 또는 채팅 ID가 설정되지 않았습니다.")
        return False

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        'chat_id': TELEGRAM_CHAT_ID,
        'text': text,
        'parse_mode': 'HTML'
    }
    try:
        response = requests.post(url, json=payload)
        if response.status_code != 200:
            print(f"텔레그램 전송 실패 ({response.status_code}): {response.text}")
            return False
        return True
    except Exception as e:
        print(f"텔레그램 요청 중 예외 발생: {e}")
        return False

def fetch_bitcoin_news():
    print(f"[{datetime.now()}] 뉴스 수집 시작... (검색어: {SEARCH_QUERY})")
    
    rss_url = f"https://news.google.com/rss/search?q={SEARCH_QUERY}&hl=ko&gl=KR&ceid=KR:ko"
    
    feed = feedparser.parse(rss_url)
    new_count = 0
    now = datetime.now(timezone.utc)
    time_limit = now - timedelta(hours=1, minutes=10)
    
    for entry in feed.entries:
        published_struct = entry.published_parsed
        published_at = datetime(*published_struct[:6], tzinfo=timezone.utc)
        
        if published_at > time_limit:
            link = entry.link
            title = html.escape(entry.title)
            
            message = f"🔔 <b>새 비트코인 뉴스</b>\n\n"
            message += f"📌 <b>제목</b>: {title}\n"
            message += f"📅 <b>날짜</b>: {entry.published}\n"
            message += f"🔗 <a href='{link}'>기사 읽기</a>"
            
            if send_telegram_message(message):
                new_count += 1
                time.sleep(1)
            
            if new_count >= 10:
                break
                
    if new_count > 0:
        print(f"{new_count}개의 새로운 뉴스를 전송했습니다.")
    else:
        print("최근 1시간 내 새로운 뉴스가 없습니다.")

def main():
    fetch_bitcoin_news()

if __name__ == "__main__":
    main()
