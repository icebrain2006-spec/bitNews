import feedparser
import requests
import time
import html
from datetime import datetime, timedelta, timezone
import config

def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{config.TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        'chat_id': config.TELEGRAM_CHAT_ID,
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
    print(f"[{datetime.now()}] 뉴스 수집 시작...")
    
    # 구글 뉴스 RSS
    rss_url = f"https://news.google.com/rss/search?q={config.SEARCH_QUERY}&hl=ko&gl=KR&ceid=KR:ko"
    
    feed = feedparser.parse(rss_url)
    new_count = 0
    
    # 현재 시간 (UTC 기준)
    now = datetime.now(timezone.utc)
    # 1시간 10분 전 기사까지 가져오기 (안전 범위)
    time_limit = now - timedelta(hours=1, minutes=10)
    
    # RSS 항목 처리 (최신순)
    for entry in feed.entries:
        # 발행 시간 파싱
        published_struct = entry.published_parsed
        published_at = datetime(*published_struct[:6], tzinfo=timezone.utc)
        
        # 설정 시간 이후의 뉴스만 처리
        if published_at > time_limit:
            link = entry.link
            title = html.escape(entry.title)
            
            # 메시지 구성 (HTML 모드)
            message = f"🔔 <b>새 비트코인 뉴스</b>\n\n"
            message += f"📌 <b>제목</b>: {title}\n"
            message += f"📅 <b>날짜</b>: {entry.published}\n"
            message += f"🔗 <a href='{link}'>기사 읽기</a>"
            
            if send_telegram_message(message):
                new_count += 1
                time.sleep(1)
            
            # 한 번에 최대 10개까지만 (너무 많이 오지 않도록)
            if new_count >= 10:
                break
                
    if new_count > 0:
        print(f"{new_count}개의 새로운 뉴스를 전송했습니다.")
    else:
        print("최근 1시간 내 새로운 뉴스가 없습니다.")

def main():
    if config.TELEGRAM_BOT_TOKEN == 'YOUR_BOT_TOKEN_HERE' or 'AAEMaJb1ZZGOzafMoC7Hq_fPG-mM0rwqMLg' not in config.TELEGRAM_BOT_TOKEN:
        if config.TELEGRAM_BOT_TOKEN == 'YOUR_BOT_TOKEN_HERE':
            print("!!! 주의: config.py 설정을 확인해주세요.")
            return

    # 한 번만 실행하고 종료 (GitHub Actions용)
    fetch_bitcoin_news()

if __name__ == "__main__":
    main()
