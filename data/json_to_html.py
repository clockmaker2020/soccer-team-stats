import os
import json

# ✅ 저장된 JSON 파일이 위치한 폴더
DATA_DIR = os.path.join(os.getcwd(), "data")

# ✅ 변환된 HTML 저장 위치
HTML_DIR = DATA_DIR  # 같은 폴더에 저장
os.makedirs(HTML_DIR, exist_ok=True)

# ✅ 1부 리그 최신 팀 목록 (강등팀 제거, 승격팀 추가)
teams = [
    "Bayern München", "Borussia Dortmund", "RB Leipzig", "Bayer Leverkusen",
    "SC Freiburg", "Union Berlin", "Eintracht Frankfurt", "VfL Wolfsburg",
    "Mainz 05", "Borussia M'gladbach", "VfL Bochum", "Werder Bremen",
    "FC Köln", "VfB Stuttgart", "FC Augsburg", "Holstein Kiel",
    "1. FC Heidenheim", "FC St. Pauli"
]

# ✅ API 요청 실패한 팀 목록 로드
failed_teams_file = os.path.join(DATA_DIR, "failed_teams.json")
failed_teams = []
if os.path.exists(failed_teams_file):
    with open(failed_teams_file, "r", encoding="utf-8") as f:
        failed_teams = json.load(f)

# ✅ JSON 데이터를 HTML로 변환하는 함수
def convert_json_to_html(team_name):
    past_file = os.path.join(DATA_DIR, f"past_matches_{team_name}.json")
    future_file = os.path.join(DATA_DIR, f"future_matches_{team_name}.json")
    html_file = os.path.join(HTML_DIR, f"update_stats_{team_name}.html")

    # ✅ API 요청 실패한 팀이면 데이터 없음 표시
    if team_name in failed_teams:
        with open(html_file, "w", encoding="utf-8") as f:
            f.write(f"""
            <html>
            <head><title>{team_name} 경기 데이터</title></head>
            <body>
                <h2>{team_name} 경기 데이터</h2>
                <p style="color: red;">⚠️ 데이터 수집 실패! 최신 경기 정보를 가져올 수 없습니다.</p>
            </body>
            </html>
            """)
        print(f"❌ {team_name} HTML 생성 (데이터 없음 표시)")
        return

    # ✅ JSON 파일 확인
    if not os.path.exists(past_file) or not os.path.exists(future_file):
        print(f"⚠️ {team_name}의 JSON 데이터가 부족하여 HTML 생성 불가.")
        return

    # ✅ JSON 파일 로드
    with open(past_file, "r", encoding="utf-8") as f:
        past_matches = json.load(f)

    with open(future_file, "r", encoding="utf-8") as f:
        future_matches = json.load(f)

    # ✅ JSON 데이터가 리스트인지 확인
    if not isinstance(past_matches, list) or not isinstance(future_matches, list):
        print(f"⚠️ {team_name}의 JSON 데이터 형식이 올바르지 않음. HTML 생성 스킵.")
        return

    # ✅ HTML 변환 (간단한 테이블 형식)
    html_content = f"""
    <html>
    <head><title>{team_name} 경기 데이터</title></head>
    <body>
        <h2>{team_name} 최근 경기 결과</h2>
        <table border='1'>
            <tr><th>날짜</th><th>홈팀</th><th>원정팀</th><th>스코어</th></tr>
    """

    for match in past_matches:
        fixture = match["fixture"]
        teams = match["teams"]
        score = match.get("score", {}).get("fulltime", {"home": "-", "away": "-"})  # ✅ 예외 처리

        html_content += f"""
            <tr>
                <td>{fixture['date'][:10]}</td>
                <td>{teams['home']['name']}</td>
                <td>{teams['away']['name']}</td>
                <td>{score['home']} - {score['away']}</td>
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
        html_content += f"""
            <tr>
                <td>{fixture['date'][:10]}</td>
                <td>{teams['home']['name']}</td>
                <td>{teams['away']['name']}</td>
            </tr>
        """

    html_content += """
        </table>
    </body>
    </html>
    """

    with open(html_file, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"✅ HTML 생성 완료: {html_file}")

# ✅ 모든 팀 변환 실행
for team in teams:
    convert_json_to_html(team)

print("🎉 모든 팀의 HTML 변환 완료!")
