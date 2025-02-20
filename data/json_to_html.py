import os
import json

# ✅ 저장된 JSON 파일이 위치한 폴더
DATA_DIR = os.path.join(os.getcwd(), "data")

# ✅ 변환된 HTML 저장 위치
HTML_DIR = DATA_DIR  # 같은 폴더에 저장
os.makedirs(HTML_DIR, exist_ok=True)

# ✅ 한글 팀명 변환 매핑
team_name_map = {
    "Bayern München": "바이에른 뮌헨",
    "Borussia Dortmund": "보루시아 도르트문트",
    "RB Leipzig": "RB 라이프치히",
    "Bayer Leverkusen": "레버쿠젠",
    "SC Freiburg": "프라이부르크",
    "Union Berlin": "우니온 베를린",
    "Eintracht Frankfurt": "프랑크푸르트",
    "VfL Wolfsburg": "볼프스부르크",
    "Mainz 05": "마인츠",
    "Borussia M'gladbach": "묀헨글라드바흐",
    "VfL Bochum": "보훔",
    "Werder Bremen": "베르더 브레멘",
    "FC Köln": "쾰른",
    "VfB Stuttgart": "슈투트가르트",
    "FC Augsburg": "아우크스부르크",
    "Holstein Kiel": "홀슈타인 킬",
    "1. FC Heidenheim": "하이덴하임",
    "FC St. Pauli": "장크트 파울리"
}

# ✅ JSON 데이터를 HTML로 변환하는 함수
def convert_json_to_html(team_name):
    past_file = os.path.join(DATA_DIR, f"past_matches_{team_name}.json")
    future_file = os.path.join(DATA_DIR, f"future_matches_{team_name}.json")
    html_file = os.path.join(HTML_DIR, f"update_stats_{team_name}.html")

    # ✅ 한글 팀명 변환
    team_name_ko = team_name_map.get(team_name, team_name)  

    # ✅ JSON 파일 확인
    if not os.path.exists(past_file) or not os.path.exists(future_file):
        print(f"⚠️ {team_name_ko}의 JSON 데이터가 부족하여 HTML 생성 불가.")
        return

    # ✅ JSON 파일 로드
    with open(past_file, "r", encoding="utf-8") as f:
        past_matches = json.load(f)

    with open(future_file, "r", encoding="utf-8") as f:
        future_matches = json.load(f)

    # ✅ HTML 변환 (한글 팀명 적용하여 표 생성)
    html_content = f"""
    <html>
    <head><title>{team_name_ko} 경기 데이터</title></head>
    <body>
        <h2>{team_name_ko} 최근 경기 결과</h2>
        <table border='1'>
            <tr><th>날짜</th><th>홈팀</th><th>원정팀</th><th>스코어</th></tr>
    """

    for match in past_matches:
        fixture = match["fixture"]
        teams = match["teams"]
        score = match["score"]
        home_team_ko = team_name_map.get(teams['home']['name'], teams['home']['name'])
        away_team_ko = team_name_map.get(teams['away']['name'], teams['away']['name'])
        html_content += f"""
            <tr>
                <td>{fixture['date'][:10]}</td>
                <td>{home_team_ko}</td>
                <td>{away_team_ko}</td>
                <td>{score['fulltime']['home']} - {score['fulltime']['away']}</td>
            </tr>
        """

    html_content += """
        </table>
        <h2>다가오는 경기</h2>
        <table border='1'>
            <tr><th>날짜</th><th>홈팀</th><th>원정팀</th></tr>
    """

    for match in future_matches:
        fixture = match["fixture"]
        teams = match["teams"]
        home_team_ko = team_name_map.get(teams['home']['name'], teams['home']['name'])
        away_team_ko = team_name_map.get(teams['away']['name'], teams['away']['name'])
        html_content += f"""
            <tr>
                <td>{fixture['date'][:10]}</td>
                <td>{home_team_ko}</td>
                <td>{away_team_ko}</td>
            </tr>
        """

    html_content += """
        </table>
    </body>
    </html>
    """

    # ✅ HTML 파일 저장
    with open(html_file, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"✅ HTML 생성 완료: {html_file}")

# ✅ 모든 팀의 JSON → HTML 변환 실행
for team in team_name_map.keys():
    convert_json_to_html(team)

print("🎉 모든 팀의 HTML 변환 완료!")
