import requests
import json
import os
import time
import html  # 🔹 추가
from datetime import datetime

# ✅ API 설정
API_KEY = "0776a35eb1067086efe59bb7f93c6498"
LEAGUE_ID = 78
SEASON = 2024
HEADERS = {"x-apisports-key": API_KEY}

# ✅ 저장 폴더 설정
SAVE_DIR = os.path.join(os.getcwd(), "data")
os.makedirs(SAVE_DIR, exist_ok=True)

# ✅ 팀 목록
teams = {
    "Bayern München": 157,
    "Borussia Dortmund": 165,
    "RB Leipzig": 173,
}

# ✅ 데이터 수집 및 저장
for team_name, team_id in teams.items():
    past_matches_url = f"https://v3.football.api-sports.io/fixtures?team={team_id}&season={SEASON}&league={LEAGUE_ID}&status=FT&last=5"
    past_matches = requests.get(past_matches_url, headers=HEADERS).json().get("response", [])
    
    if past_matches:
        with open(os.path.join(SAVE_DIR, f"past_matches_{team_name}.json"), "w", encoding="utf-8") as file:
            json.dump(past_matches, file, indent=4, ensure_ascii=False)

# ✅ HTML 변환 후 JSON 저장
post_data = {"content": "<h3>📌 최근 경기 결과</h3><table border='1'><tr><th>날짜</th><th>홈팀</th><th>스코어</th><th>원정팀</th></tr>"}

for team_name in teams.keys():
    past_file = os.path.join(SAVE_DIR, f"past_matches_{team_name}.json")
    if os.path.exists(past_file):
        with open(past_file, "r", encoding="utf-8") as f:
            past_matches = json.load(f)

        for match in past_matches[:5]:  
            fixture = match["fixture"]
            teams_info = match["teams"]
            score = match["score"]
            post_data["content"] += (
                f"<tr><td>{html.escape(fixture['date'][:10])}</td>"
                f"<td>{html.escape(teams_info['home']['name'])}</td>"
                f"<td>{html.escape(str(score['fulltime']['home']))} - {html.escape(str(score['fulltime']['away']))}</td>"
                f"<td>{html.escape(teams_info['away']['name'])}</td></tr>"
            )

post_data["content"] += "</table>"

# ✅ post_data.json 저장
with open(os.path.join(SAVE_DIR, "post_data.json"), "w", encoding="utf-8") as file:
    json.dump(post_data, file, indent=4, ensure_ascii=False)

print(f"✅ post_data.json 업데이트 완료")
