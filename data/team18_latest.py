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

# ✅ UTC 시간을 KST(한국 시간)으로 변환하는 함수 추가
def convertToKST(utc_date):
    date = datetime.strptime(utc_date, "%Y-%m-%dT%H:%M:%S%z")
    kst_date = date.astimezone().strftime("%Y-%m-%d %H:%M")  # ✅ KST 변환
    return kst_date

# ✅ 1부 리그 팀 자동 검색
def get_top_league_teams():
    url = f"https://v3.football.api-sports.io/standings?league={LEAGUE_ID}&season={SEASON}"
    response = requests.get(url, headers=HEADERS)
    data = response.json()
    
    teams = {}
    for team in data.get("response", [])[0]["league"]["standings"][0]:  # 1부 리그 팀 가져오기
        teams[team["team"]["name"]] = team["team"]["id"]
    
    return teams

# ✅ API 요청 함수
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
teams = get_top_league_teams()

# ✅ 팀별 최종 경기 데이터 가져오기
latest_matches = []

for team_name, team_id in teams.items():
    print(f"📌 {team_name} 경기 데이터 조회 중...")

    latest_match_url = f"https://v3.football.api-sports.io/fixtures?team={team_id}&season={SEASON}&league={LEAGUE_ID}&status=FT&last=1"
    past_matches_url = f"https://v3.football.api-sports.io/fixtures?team={team_id}&season={SEASON}&league={LEAGUE_ID}&status=FT&last=5"
    future_matches_url = f"https://v3.football.api-sports.io/fixtures?team={team_id}&season={SEASON}&league={LEAGUE_ID}&status=NS&next=3"
    squad_url = f"https://v3.football.api-sports.io/players/squads?team={team_id}&season={SEASON}"

    match_data = fetch_data(latest_match_url)
    past_matches = fetch_data(past_matches_url)
    future_matches = fetch_data(future_matches_url)
    squad_data = fetch_data(squad_url)

    if match_data:
        match = match_data[0]  # ✅ 최신 경기 1개 선택
        fixture_date_kst = convertToKST(match["fixture"]["date"])  # ✅ KST 변환 적용

        # ✅ 경기 상세 정보 요청
        fixture_id = match["fixture"]["id"]
        fixture_detail_url = f"https://v3.football.api-sports.io/fixtures?id={fixture_id}"
        fixture_detail = fetch_data(fixture_detail_url)[0] if fetch_data(fixture_detail_url) else {}

        # ✅ 추가 데이터 가져오기
        stadium = fixture_detail.get("fixture", {}).get("venue", {}).get("name", "미정")
        referee = fixture_detail.get("fixture", {}).get("referee", "정보 없음")
        league_round = fixture_detail.get("league", {}).get("round", "라운드 정보 없음")

        # ✅ 주요 경기 이벤트 가져오기
        events = fixture_detail.get("events", [])
        event_list = []
        for event in events:
            event_list.append({
                "time": f"{event['time']['elapsed']}'",
                "player": event['player']['name'],
                "detail": event['detail'],
                "team": event['team']['name']
            })
        
        # ✅ 배당률 정보 가져오기
        odds = fixture_detail.get("odds", {}).get("1X2", {})
        home_odds = odds.get("home", "N/A")
        draw_odds = odds.get("draw", "N/A")
        away_odds = odds.get("away", "N/A")

        # ✅ 최근 5경기 데이터 추가 (KST 변환)
        past_results = [{"date": convertToKST(m["fixture"]["date"]), "score": f"{m['score']['fulltime']['home']} - {m['score']['fulltime']['away']}"} for m in past_matches]

        # ✅ 향후 3경기 일정 추가 (KST 변환)
        future_games = [{"date": convertToKST(m["fixture"]["date"]), "opponent": m["teams"]["away"]["name"] if m["teams"]["home"]["name"] == team_name else m["teams"]["home"]["name"]} for m in future_matches]

        # ✅ 주요 선수 데이터 추가
        squad_list = [{"name": player["player"]["name"], "position": player["statistics"][0]["games"]["position"]} for player in squad_data[0]["players"]] if squad_data else []

        latest_matches.append({
            "team": team_name,
            "date": fixture_date_kst,
            "opponent": match["teams"]["away"]["name"] if match["teams"]["home"]["name"] == team_name else match["teams"]["home"]["name"],
            "score": f"{match['score']['fulltime']['home']} - {match['score']['fulltime']['away']}",
            "stadium": stadium,
            "referee": referee,
            "league_round": league_round,
            "events": event_list,
            "odds": {"home": home_odds, "draw": draw_odds, "away": away_odds},
            "past_results": past_results,
            "future_games": future_games,
            "squad": squad_list
        })

# ✅ JSON 저장
with open(os.path.join(SAVE_DIR, "team18_latest.json"), "w", encoding="utf-8") as file:
    json.dump({"latest_matches": latest_matches}, file, indent=4, ensure_ascii=False)

print("✅ JSON 파일 저장 완료!")
