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

# ✅ 1부 리그 팀 목록 가져오기
def get_bundesliga_teams():
    url = f"https://v3.football.api-sports.io/teams?league={LEAGUE_ID}&season={SEASON}"
    response = requests.get(url, headers=HEADERS)
    teams_data = response.json().get("response", [])

    teams = {}
    for team in teams_data:
        team_name = team["team"]["name"]
        team_id = team["team"]["id"]
        teams[team_name] = team_id

    return teams

# ✅ 경기 데이터 가져오기 함수 (재시도 포함)
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

# ✅ 경기 날짜 기준 정렬 함수
def sort_by_date(match):
    return datetime.strptime(match["fixture"]["date"], "%Y-%m-%dT%H:%M:%S%z")

# ✅ 1부 리그 팀 자동 검색
teams = get_bundesliga_teams()
print(f"🎯 1부 리그 18개 팀 자동 검색 완료: {list(teams.keys())}")

# ✅ 각 팀별 최신 경기 찾기
latest_matches = []

for team_name, team_id in teams.items():
    print(f"📌 {team_name} 최종 경기 데이터 조회 중...")

    # ✅ 팀의 가장 최근 완료된 경기 가져오기
    latest_match_url = f"https://v3.football.api-sports.io/fixtures?team={team_id}&season={SEASON}&league={LEAGUE_ID}&status=FT&last=1"
    match_data = fetch_data(latest_match_url)

    if match_data:
        match = match_data[0]  # ✅ 최신 경기 1개 선택
        fixture_date = datetime.strptime(match["fixture"]["date"], "%Y-%m-%dT%H:%M:%S%z")
        fixture_date_kst = fixture_date.astimezone().strftime("%Y-%m-%d %H:%M")  # ✅ 한국시간 변환

        latest_matches.append({
            "team": team_name,
            "date": fixture_date_kst,
            "opponent": match["teams"]["away"]["name"] if match["teams"]["home"]["name"] == team_name else match["teams"]["home"]["name"],
            "score": f"{match['score']['fulltime']['home']} - {match['score']['fulltime']['away']}"
        })

# ✅ JSON 데이터 저장 (data/team_data/team18_latest.json)
output_file_path = os.path.join(SAVE_DIR, "team18_latest.json")
with open(output_file_path, "w", encoding="utf-8") as file:
    json.dump({"latest_matches": latest_matches}, file, indent=4, ensure_ascii=False)

print(f"✅ 최종 경기 데이터 저장 완료: {output_file_path}")
