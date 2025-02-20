import requests
import json
import os
from datetime import datetime

# ✅ API 설정
API_KEY = os.getenv("SOCCER_STATS_API")  # 환경 변수에서 API 키 가져오기
LEAGUE_ID = 78  # 분데스리가 ID
SEASON = 2024  # 최신 시즌
HEADERS = {"x-apisports-key": API_KEY}

# ✅ 저장 폴더 설정
SAVE_DIR = os.path.join(os.getcwd(), "data")
os.makedirs(SAVE_DIR, exist_ok=True)

# ✅ 추적할 팀 목록
teams = {
    "Bayern München": 157,
    "Borussia Dortmund": 165,
    "RB Leipzig": 173,
    "Bayer Leverkusen": 168,
    "SC Freiburg": 160,
    "Union Berlin": 182,
    "Eintracht Frankfurt": 159,
    "VfL Wolfsburg": 174,
    "Mainz 05": 164,
    "Borussia M'gladbach": 163,
    "VfL Bochum": 170,
    "Werder Bremen": 166,
    "FC Köln": 167,
    "VfB Stuttgart": 172,
    "FC Augsburg": 161,
    "Hertha BSC": 183,
    "Schalke 04": 185,
    "Holstein Kiel": 264
}

# ✅ API 데이터 요청 함수
def fetch_data(url):
    response = requests.get(url, headers=HEADERS)
    data = response.json()
    return data.get("response", [])

# ✅ 모든 팀의 경기 데이터를 가져오기
for team_name, team_id in teams.items():
    print(f"📌 {team_name} 경기 데이터 수집 중...")

    # ✅ 최근 5경기 결과 가져오기
    past_matches_url = f"https://v3.football.api-sports.io/fixtures?team={team_id}&season={SEASON}&league={LEAGUE_ID}&status=FT&last=5"
    past_matches = fetch_data(past_matches_url)

    # ✅ 향후 3경기 일정 가져오기
    future_matches_url = f"https://v3.football.api-sports.io/fixtures?team={team_id}&season={SEASON}&league={LEAGUE_ID}&status=NS&next=3"
    future_matches = fetch_data(future_matches_url)

    # ✅ 데이터 저장
    with open(os.path.join(SAVE_DIR, f"past_matches_{team_name}.json"), "w", encoding="utf-8") as file:
        json.dump(past_matches, file, indent=4, ensure_ascii=False)

    with open(os.path.join(SAVE_DIR, f"future_matches_{team_name}.json"), "w", encoding="utf-8") as file:
        json.dump(future_matches, file, indent=4, ensure_ascii=False)

    print(f"✅ 경기 데이터 저장 완료: {team_name}")

print("🎉 모든 팀의 경기 데이터 업데이트 완료!")
