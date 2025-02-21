import requests
import json
import os
import time
import html
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

# ✅ API 요청 함수
def fetch_data(url):
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        return response.json().get("response", [])
    except requests.exceptions.RequestException as e:
        print(f"⚠️ [ERROR] API 요청 오류: {e}")
        return []

# ✅ 데이터 수집 및 저장
for team_name, team_id in teams.items():
    print(f"📌 {team_name} 경기 데이터 수집 중...")

    past_matches_url = f"https://v3.football.api-sports.io/fixtures?team={team_id}&season={SEASON}&league={LEAGUE_ID}&status=FT&last=5"
    past_matches = fetch_data(past_matches_url)
    time.sleep(1)  # ⏳ 1초 대기 후 다음 요청

    if past_matches:
        with open(os.path.join(SAVE_DIR, f"past_matches_{team_name}.json"), "w", encoding="utf-8") as file:
            json.dump(past_matches, file, indent=4, ensure_ascii=False)

        print(f"✅ [SUCCESS] {team_name} 경기 데이터 저장 완료!")
    else:
        print(f"❌ [FAILED] {team_name} 경기 데이터 수집 실패!")

# ✅ HTML 변환 후 JSON 저장
post_data = {"content": "<h3>📌 최근 경기 결과</h3>"}

# ✅ `soccer-table` 클래스를 추가하여 티스토리 스타일과 충돌 방지
post_data["content"] += """
<table class='soccer-table'>
<tr>
    <th>날짜</th>
    <th>홈팀</th>
    <th>스코어</th>
    <th>원정팀</th>
</tr>
"""

for team_name in teams.keys():
    past_file = os.path.join(SAVE_DIR, f"past_matches_{team_name}.json")
    if os.path.exists(past_file):
        with open(past_file, "r", encoding="utf-8") as f:
            past_matches = json.load(f)

        for match in past_matches[:5]:  # ✅ 최근 5경기만 포함
            fixture = match["fixture"]
            teams_info = match["teams"]
            score = match["score"]
            post_data["content"] += f"""
            <tr>
                <td>{html.escape(fixture['date'][:10])}</td>
                <td>{html.escape(teams_info['home']['name'])}</td>
                <td>{html.escape(str(score['fulltime']['home']))} - {html.escape(str(score['fulltime']['away']))}</td>
                <td>{html.escape(teams_info['away']['name'])}</td>
            </tr>
            """

post_data["content"] += "</table>"

# ✅ `post_data.json` 저장
post_data_file = os.path.join(SAVE_DIR, "post_data.json")
with open(post_data_file, "w", encoding="utf-8") as file:
    json.dump(post_data, file, indent=4, ensure_ascii=False)

print(f"✅ post_data.json이 업데이트되었습니다: {post_data_file}")
