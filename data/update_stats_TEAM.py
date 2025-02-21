import os
import json
import requests
import time
from datetime import datetime

# ✅ API 설정
API_KEY = "0776a35eb1067086efe59bb7f93c6498"
LEAGUE_ID = 78  # 분데스리가 ID
SEASON = 2024  # 최신 시즌
HEADERS = {"x-apisports-key": API_KEY}

# ✅ 저장 폴더 설정
SAVE_DIR = os.path.join(os.getcwd(), "data/team_data")
os.makedirs(SAVE_DIR, exist_ok=True)

# ✅ 추적할 팀 목록
teams = {
    "Bayern München": 157,
    "Borussia Dortmund": 165,
    "RB Leipzig": 173,
    "Bayer Leverkusen": 168,
    "SC Freiburg": 160,
    "Union Berlin": 182,
    "Eintracht Frankfurt": 169,
    "VfL Wolfsburg": 161,
    "Mainz 05": 164,
    "Borussia M'gladbach": 163,
    "VfL Bochum": 176,
    "Werder Bremen": 162,
    "FC Köln": 170,
    "VfB Stuttgart": 172,
    "FC Augsburg": 170,
    "Holstein Kiel": 191,
    "1. FC Heidenheim": 180,
    "FC St. Pauli": 186,
}

# ✅ API 요청 함수 (재시도 포함)
def fetch_data(url, retries=3):
    for attempt in range(retries):
        try:
            response = requests.get(url, headers=HEADERS, timeout=10)
            response.raise_for_status()
            return response.json().get("response", [])
        except requests.exceptions.RequestException as e:
            print(f"⚠️ [ERROR] API 요청 오류 (시도 {attempt+1}/{retries}): {e}")
            time.sleep(3)  # ⏳ 3초 대기 후 재시도
    return []

# ✅ 각 팀별 JSON 파일 생성
for team_name, team_id in teams.items():
    print(f"📌 {team_name} 경기 데이터 수집 중...")

    # 최근 5경기 데이터 가져오기 (완료된 경기)
    past_matches_url = f"https://v3.football.api-sports.io/fixtures?team={team_id}&season={SEASON}&league={LEAGUE_ID}&status=FT&last=5"
    past_matches = fetch_data(past_matches_url)
    time.sleep(1)  # ⏳ 1초 대기 후 다음 요청

    # 향후 3경기 데이터 가져오기 (예정된 경기)
    future_matches_url = f"https://v3.football.api-sports.io/fixtures?team={team_id}&season={SEASON}&league={LEAGUE_ID}&status=NS&next=3"
    future_matches = fetch_data(future_matches_url)
    time.sleep(1)

    # ✅ JSON 데이터 구조 생성
    team_data = {
        "team": team_name,
        "past_matches": past_matches,  # 지난 경기 5개
        "future_matches": future_matches  # 향후 경기 3개
    }

    # ✅ 팀별 JSON 파일 저장 (파일명: team_팀이름.json)
    file_name = f"team_{team_name.replace(' ', '').replace('.', '')}.json"
    team_file_path = os.path.join(SAVE_DIR, file_name)

    with open(team_file_path, "w", encoding="utf-8") as file:
        json.dump(team_data, file, indent=4, ensure_ascii=False)

    print(f"✅ {team_name} 데이터 저장 완료: {team_file_path}")

# ✅ 모든 팀 데이터 저장 완료
print("🎉 모든 팀별 JSON 파일 생성 완료!")
