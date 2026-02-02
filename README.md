# 비트코인 뉴스 텔레그램 알림 봇

이 프로그램은 1시간마다 구글 뉴스에서 '비트코인' 관련 뉴스를 수집하여 텔레그램으로 전송해줍니다.

## 1. 사전 준비 (텔레그램 설정)

### 1.1 텔레그램 봇 만들기
1. 텔레그램에서 [@BotFather](https://t.me/botfather)를 검색합니다.
2. `/newbot` 명령어를 입력합니다.
3. 봇의 이름과 사용자 이름(username, 'bot'으로 끝나야 함)을 설정합니다.
4. 생성 완료 후 제공되는 **HTTP API token**을 복사하여 `config.py`의 `TELEGRAM_BOT_TOKEN`에 넣습니다.

### 1.2 채팅 ID(Chat ID) 확인하기
1. 텔레그램에서 방금 만든 봇을 검색해 **Start**를 누릅니다.
2. [@userinfobot](https://t.me/userinfobot)을 검색해 **Start**를 누르면 본인의 `Id`를 알려줍니다.
3. 이 숫자를 `config.py`의 `TELEGRAM_CHAT_ID`에 넣습니다.

## 2. 설치 및 실행

### 2.1 라이브러리 설치
터미널에서 다음 명령어를 실행하여 필요한 패키지를 설치합니다:
```bash
pip install -r requirements.txt
```

### 2.2 프로그램 실행
```bash
python main.py
```

## 3. 설정 변경 (`config.py`)
- `SEARCH_QUERY`: 검색어 변경 가능 (예: '이더리움', '가상화폐' 등)
- `INTERVAL_HOURS`: 알림 주기 변경 가능 (기본 1시간)
