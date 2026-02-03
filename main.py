import feedparser
import requests
import time
import html
import os
from datetime import datetime, timedelta, timezone

# 환경변수(GitHub Secrets)를 최우선으로 사용하고, 없으면 config.py 사용
def get_setting(key, default=None):
    # 1. 환경변수 확인
    val = os.environ.get(key)
    if val:
        return val
    # 2. config.py 확인
    try:
        import config
        return getattr(config, key, default)
    except ImportError:
        return default

TELEGRAM_BOT_TOKEN = get_setting('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = get_setting('TELEGRAM_CHAT_ID')
SEARCH_QUERY = get_setting('SEARCH_QUERY', '비트코인')

def send_telegram_message(text):
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("에러: 설정값이 부족합니다. Secrets 설정을 확인하세요.")
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
            print(f"전송 실패 ({response.status_code}): {response.text}")
            return False
        return True
    except Exception as e:
        print(f"예외 발생: {e}")
        return False

def fetch_bitcoin_news():
    print(f"[{datetime.now()}] 뉴스 수집 시작... (검색어: {SEARCH_QUERY})")
    rss_url = f"https://news.google.com/rss/search?q={SEARCH_QUERY}&hl=ko&gl=KR&ceid=KR:ko"
    
    feed = feedparser.parse(rss_url)
    new_count = 0
    now = datetime.now(timezone.utc)
    # 한 시간보다 조금 넉넉하게 70분 전 뉴스까지 수집
    time_limit = now - timedelta(minutes=70)
    
    for entry in feed.entries:
        try:
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
                
                if new_count >= 10: break
        except Exception as e:
            print(f"뉴스 처리 중 오류: {e}")
            continue
                
    if new_count > 0:
        print(f"{new_count}개의 뉴스를 전송했습니다.")
    else:
        print("새로운 뉴스가 없습니다.")

def main():
    fetch_bitcoin_news()

if __name__ == "__main__":
    main()
