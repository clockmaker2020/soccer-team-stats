import os
import json

# ✅ 저장된 JSON 파일이 위치한 폴더
DATA_DIR = os.path.join(os.getcwd(), "data")

# ✅ 변환된 HTML 저장 위치
HTML_DIR = DATA_DIR  # 같은 폴더에 저장
os.makedirs(HTML_DIR, exist_ok=True)

# ✅ 한글 폰트 설정
FONT_CSS = """
@font-face {
    font-family: 'Noto Sans KR';
    font-style: normal;
    font-weight: 400;
    src: url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;700&display=swap');
}
body {
    font-family: 'Noto Sans KR', sans-serif;
    background: transparent;
    color: #333;
    text-align: center;
}
h3 {
    font-size: 22px;
    font-weight: bold;
    margin-bottom: 10px;
}
table {
    width: 100%;
    border-collapse: collapse;
    table-layout: fixed;
    font-size: 18px;
}
th, td {
    padding: 10px;
    border: 1px solid #ddd;
}
th {
    background: #ffcc99;
    font-weight: bold;
}
"""
# ✅ 추적할 팀 목록
teams = [
    "Bayern München", "Borussia Dortmund", "RB Leipzig", "Bayer Leverkusen",
    "SC Freiburg", "Union Berlin", "Eintracht Frankfurt", "VfL Wolfsburg",
    "Mainz 05", "Borussia M'gladbach", "VfL Bochum", "Werder Bremen",
    "FC Köln", "VfB Stuttgart", "FC Augsburg", "Hertha BSC", "Schalke 04",
    "Holstein Kiel"
]

# ✅ JSON 데이터를 HTML로 변환하는 함수
def convert_json_to_html(team_name):
    past_file = os.path.join(DATA_DIR, f"past_matches_{team_name}.json")
    future_file = os.path.join(DATA_DIR, f"future_matches_{team_name}.json")
    html_file = os.path.join(HTML_DIR, f"update_stats_{team_name}.html")

    if not os.path.exists(past_file) or not os.path.exists(future_file):
        print(f"⚠️ {team_name}의 JSON 데이터가 부족하여 HTML 생성 불가.")
        return

    # ✅ JSON 파일 로드
    with open(past_file, "r", encoding="utf-8") as f:
        past_matches = json.load(f)

    with open(future_file, "r", encoding="utf-8") as f:
        future_matches = json.load(f)

    # ✅ HTML 변환 (테이블 포함)
    html_content = f"""
    <html>
    <head>
        <meta charset="utf-8">
        <title>{team_name} 경기 데이터</title>
        <style>{FONT_CSS}</style>
    </head>
    <body>
        <h3>📌 최근 5경기 결과</h3>
        <table>
            <tr><th>날짜</th><th>홈팀</th><th>스코어</th><th>원정팀</th></tr>
    """

    for match in past_matches:
        fixture = match["fixture"]
        teams = match["teams"]
        score = match["score"]
        html_content += f"""
            <tr>
                <td>{fixture['date'][:10]}</td>
                <td>{teams['home']['name']}</td>
                <td>{score['fulltime']['home']} - {score['fulltime']['away']}</td>
                <td>{teams['away']['name']}</td>
            </tr>
        """

    html_content += """
        </table>
        <h3>📌 향후 3경기 일정</h3>
        <table>
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

    # ✅ HTML 파일 저장
    with open(html_file, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"✅ HTML 생성 완료: {html_file}")

# ✅ 모든 팀의 JSON → HTML 변환 실행
for team in teams:
    convert_json_to_html(team)

print("🎉 모든 팀의 HTML 변환 완료!")
