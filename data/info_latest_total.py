import os
import json
import requests
import time

# ✅ API 설정
API_KEY = "0776a35eb1067086efe59bb7f93c6498"  # ⚠ 실제 API 키 입력
LEAGUE_ID = 78  # 분데스리가 ID
SEASON = 2024  # 최신 시즌
HEADERS = {"x-apisports-key": API_KEY}

# ✅ 저장 폴더 설정
SAVE_DIR = os.path.join(os.getcwd(), "data/team_data")
os.makedirs(SAVE_DIR, exist_ok=True)

# ✅ 18개 팀 목록 (팀명: 팀 ID)
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
    "1899 Hoffenheim": 167,
    "VfB Stuttgart": 172,
    "FC Augsburg": 170,
    "Holstein Kiel": 191,
    "1. FC Heidenheim": 180,
    "FC St. Pauli": 186,
}

# ✅ API 요청 함수 (최대 3회 재시도)
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

# ✅ 각 팀별 최신 경기 데이터 저장
for team_name, team_id in teams.items():
    print(f"📌 {team_name} 최신 경기 데이터 수집 중...")

    # 최신 경기 1개 가져오기 (완료된 경기)
    match_url = f"https://v3.football.api-sports.io/fixtures?team={team_id}&season={SEASON}&league={LEAGUE_ID}&status=FT&last=1"
    matches = fetch_data(match_url)

    if not matches:
        print(f"⚠️ {team_name} 경기 데이터를 찾을 수 없습니다. 건너뜀.")
        continue

    latest_match = matches[0]  # 가장 최근 경기
    fixture = latest_match.get("fixture", {})
    league = latest_match.get("league", {})
    teams_info = latest_match.get("teams", {})
    score = latest_match.get("score", {})
    events = latest_match.get("events", [])
    statistics = latest_match.get("statistics", [])
    lineups = latest_match.get("lineups", [])
    odds = latest_match.get("odds", [])

    # ✅ JSON 데이터 구조 생성
    team_data = {
        "fixture": {
            "id": fixture.get("id", "N/A"),
            "date": fixture.get("date", "N/A"),
            "venue": {
                "name": fixture.get("venue", {}).get("name", "Unknown"),
                "city": fixture.get("venue", {}).get("city", "Unknown"),
            },
            "referee": fixture.get("referee", "Unknown"),
        },
        "league": {
            "name": league.get("name", "Unknown"),
            "season": league.get("season", "Unknown"),
            "round": league.get("round", "Unknown"),
        },
        "teams": {
            "home": {
                "id": teams_info.get("home", {}).get("id", "N/A"),
                "name": teams_info.get("home", {}).get("name", "N/A"),
                "logo": teams_info.get("home", {}).get("logo", "N/A"),
            },
            "away": {
                "id": teams_info.get("away", {}).get("id", "N/A"),
                "name": teams_info.get("away", {}).get("name", "N/A"),
                "logo": teams_info.get("away", {}).get("logo", "N/A"),
            },
        },
        "score": {
            "halftime": score.get("halftime", {"home": 0, "away": 0}),
            "fulltime": score.get("fulltime", {"home": 0, "away": 0}),
            "extratime": score.get("extratime", {"home": 0, "away": 0}),
            "penalty": score.get("penalty", {"home": 0, "away": 0}),
        },
        "status": {
            "long": fixture.get("status", {}).get("long", "Unknown"),
            "elapsed": fixture.get("status", {}).get("elapsed", "N/A"),
        },
        "events": events,
        "statistics": statistics,
        "lineups": lineups,
        "odds": odds,
    }

    # ✅ 팀별 JSON 파일 저장 (`info_팀명.json` 형식)
    file_name = f"info_{team_name.replace(' ', '').replace('.', '')}.json"
    team_file_path = os.path.join(SAVE_DIR, file_name)

    with open(team_file_path, "w", encoding="utf-8") as file:
        json.dump(team_data, file, indent=4, ensure_ascii=False)

    print(f"✅ {team_name} 최신 경기 데이터 저장 완료: {team_file_path}")

# ✅ 모든 팀 데이터 저장 완료
print("🎉 모든 팀별 JSON 데이터 업데이트 완료!")
