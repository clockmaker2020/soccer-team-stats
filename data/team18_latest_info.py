import os
import json
import requests
import time
from datetime import datetime

# ✅ API 설정
API_KEY = "0776a35eb1067086efe59bb7f93c6498"
LEAGUE_ID = 78
SEASON = 2024
HEADERS = {"x-apisports-key": API_KEY}

# ✅ 저장 폴더 설정
SAVE_DIR = os.path.join(os.getcwd(), "data/team_data")
os.makedirs(SAVE_DIR, exist_ok=True)

# ✅ UTC 시간을 KST(한국 시간)으로 변환하는 함수
def convertToKST(utc_date):
    date = datetime.strptime(utc_date, "%Y-%m-%dT%H:%M:%S%z")
    return date.astimezone().strftime("%Y-%m-%d %H:%M")

# ✅ API 요청 함수 (재시도 포함)
def fetch_data(url, retries=3):
    for attempt in range(retries):
        try:
            response = requests.get(url, headers=HEADERS, timeout=10)
            response.raise_for_status()
            return response.json().get("response", [])
        except requests.exceptions.RequestException as e:
            print(f"⚠️ [ERROR] API 요청 오류 (시도 {attempt+1}/{retries}): {e}")
            time.sleep(3)
    return []

# ✅ 1부 리그 팀 목록 가져오기
def get_top_league_teams():
    url = f"https://v3.football.api-sports.io/standings?league={LEAGUE_ID}&season={SEASON}"
    response = requests.get(url, headers=HEADERS)
    data = response.json()
    
    teams = {}
    for team in data.get("response", [])[0]["league"]["standings"][0]:
        teams[team["team"]["name"]] = team["team"]["id"]
    
    return teams

# ✅ 팀 데이터 저장
teams = get_top_league_teams()
latest_matches = []

for team_name, team_id in teams.items():
    print(f"📌 {team_name} 경기 데이터 조회 중...")

    # ✅ API 요청 URL 목록
    latest_match_url = f"https://v3.football.api-sports.io/fixtures?team={team_id}&season={SEASON}&league={LEAGUE_ID}&status=FT&last=1"
    injuries_url = f"https://v3.football.api-sports.io/injuries?league={LEAGUE_ID}&season={SEASON}&team={team_id}"

    # ✅ 데이터 가져오기
    match_data = fetch_data(latest_match_url)
    injuries = fetch_data(injuries_url)

    if match_data:
        match = match_data[0]
        fixture_date_kst = convertToKST(match["fixture"]["date"])
        fixture_id = match["fixture"]["id"]

        # ✅ 경기 상세 정보 요청
        fixture_detail_url = f"https://v3.football.api-sports.io/fixtures?id={fixture_id}"
        fixture_detail = fetch_data(fixture_detail_url)[0] if fetch_data(fixture_detail_url) else {}

        stadium = fixture_detail.get("fixture", {}).get("venue", {}).get("name", "미정")
        referee = fixture_detail.get("fixture", {}).get("referee", "정보 없음")
        league_round = fixture_detail.get("league", {}).get("round", "라운드 정보 없음")

        # ✅ 주요 경기 이벤트 가져오기
        events = fixture_detail.get("events", [])
        event_list = [{"time": f"{e['time']['elapsed']}'", "player": e['player']['name'], "detail": e['detail'], "team": e['team']['name']} for e in events]

        # ✅ 부상 선수 정보 가져오기 (예외 처리 추가)
        injury_list = []
        for inj in injuries:
            player_name = inj.get("player", {}).get("name", "이름 없음")
            injury_type = inj.get("type", "정보 없음")
            return_date = inj.get("fixture", {}).get("date", "미정")

            injury_list.append({
                "player": player_name,
                "type": injury_type,
                "return": return_date
            })

        # ✅ JSON 데이터 저장
        latest_matches.append({
            "team": team_name,
            "date": fixture_date_kst,
            "opponent": match["teams"]["away"]["name"] if match["teams"]["home"]["name"] == team_name else match["teams"]["home"]["name"],
            "score": f"{match['score']['fulltime']['home']} - {match['score']['fulltime']['away']}",
            "stadium": stadium,
            "referee": referee,
            "league_round": league_round,
            "events": event_list,
            "injuries": injury_list
        })

# ✅ JSON 저장
with open(os.path.join(SAVE_DIR, "team18_latest_info.json"), "w", encoding="utf-8") as file:
    json.dump({"latest_matches": latest_matches}, file, indent=4, ensure_ascii=False)

print("✅ JSON 파일 저장 완료!")
