import requests
import json
import os
import time
from datetime import datetime

# ✅ API 설정
API_KEY = "0776a35eb1067086efe59bb7f93c6498"
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

# ✅ API 요청 실패한 팀 목록
failed_teams = []

# ✅ API 데이터 요청 함수
def fetch_data(url):
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)  # ⏳ 10초 제한
        response.raise_for_status()  # 🚨 HTTP 오류 발생 시 예외 처리
        data = response.json()
        return data.get("response", [])
    except requests.exceptions.Timeout:
        print(f"⚠️ [TIMEOUT] API 응답 없음: {url}")
        return []
    except requests.exceptions.RequestException as e:
        print(f"⚠️ [ERROR] API 요청 오류: {e}")
        return []

# ✅ 모든 팀의 경기 데이터를 가져오기
for team_name, team_id in teams.items():
    print(f"📌 {team_name} 경기 데이터 수집 중...")

    past_matches_url = f"https://v3.football.api-sports.io/fixtures?team={team_id}&season={SEASON}&league={LEAGUE_ID}&status=FT&last=5"
    future_matches_url = f"https://v3.football.api-sports.io/fixtures?team={team_id}&season={SEASON}&league={LEAGUE_ID}&status=NS&next=3"

    past_matches = fetch_data(past_matches_url)
    time.sleep(1)  # ⏳ 1초 대기 후 다음 요청
    future_matches = fetch_data(future_matches_url)
    time.sleep(1)

    if not past_matches or not future_matches:
        print(f"❌ [FAILED] {team_name} 경기 데이터 수집 실패!")
        failed_teams.append(team_name)  # ❌ 실패한 팀 저장
    else:
        # ✅ 정상적으로 데이터를 가져온 경우 JSON 저장
        with open(os.path.join(SAVE_DIR, f"past_matches_{team_name}.json"), "w", encoding="utf-8") as file:
            json.dump(past_matches, file, indent=4, ensure_ascii=False)

        with open(os.path.join(SAVE_DIR, f"future_matches_{team_name}.json"), "w", encoding="utf-8") as file:
            json.dump(future_matches, file, indent=4, ensure_ascii=False)

        print(f"✅ [SUCCESS] {team_name} 경기 데이터 저장 완료!")

# ✅ API 요청 실패한 팀 목록을 JSON으로 저장
failed_teams_file = os.path.join(SAVE_DIR, "failed_teams.json")
with open(failed_teams_file, "w", encoding="utf-8") as f:
    json.dump(failed_teams, f, indent=4, ensure_ascii=False)

# ✅ API 요청 실패한 팀 목록 출력
if failed_teams:
    print("\n❌ [FAILED TEAMS] 데이터 수집 실패한 팀 목록:")
    for team in failed_teams:
        print(f"- {team}")
else:
    print("\n✅ 모든 팀의 데이터가 정상적으로 수집되었습니다!")

print(f"✅ 실패한 팀 목록 저장 완료: {failed_teams_file}")
print("🎉 모든 팀의 경기 데이터 업데이트 완료!")
