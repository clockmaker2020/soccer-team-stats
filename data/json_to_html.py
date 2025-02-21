import os
import json

# ✅ 저장된 JSON 파일이 위치한 폴더
DATA_DIR = os.path.join(os.getcwd(), "data")

# ✅ 변환된 HTML 저장 위치
HTML_DIR = DATA_DIR  # 같은 폴더에 저장
os.makedirs(HTML_DIR, exist_ok=True)

# ✅ 팀명 한글 변환 (2024-25 시즌 기준)
team_translation = {
    "Bayern München": "바이에른 뮌헨",
    "Borussia Dortmund": "도르트문트",
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
    "Hertha BSC": "헤르타 BSC",
    "Schalke 04": "샬케 04",
    "Holstein Kiel": "홀슈타인 킬"
}

# ✅ 추적할 팀 목록
teams = list(team_translation.keys())

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
    html_file = os.path.join(HTML_DIR, f"update_stats_{team_translation.get(team_name, team_name)}.html")

    # ✅ API 요청 실패한 팀이면 데이터 없음 표시
    if team_name in failed_teams:
        with open(html_file, "w", encoding="utf-8") as f:
            f.write(f"""
            <html>
            <head>
                <title>{team_translation.get(team_name, team_name)} 경기 데이터</title>
                <style>
                    body {{
                        font-family: Arial, sans-serif;
                        margin: 0;
                        padding: 0;
                        text-align: center;
                        background: white;
                    }}
                    h3 {{
                        font-size: 26px;
                        font-weight: bold;
                        margin-top: 20px;
                    }}
                    table {{
                        width: 100%;
                        max-width: 1000px;
                        margin: auto;
                        border-collapse: collapse;
                        font-size: 22px;
                    }}
                    th, td {{
                        border: 1px solid black;
                        padding: 15px;
                        text-align: center;
                    }}
                    th {{
                        background-color: #ffcc99;
                        font-weight: bold;
                    }}
                </style>
            </head>
            <body>
                <h3>📌 {team_translation.get(team_name, team_name)} 경기 데이터</h3>
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

    # ✅ HTML 변환 (모바일 최적화, 컬럼 추가)
    html_content = f"""
    <html>
    <head>
        <title>{team_translation.get(team_name, team_name)} 경기 데이터</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 0;
                text-align: center;
                background: white;
            }}
            h3 {{
                font-size: 26px;
                font-weight: bold;
                margin-top: 20px;
            }}
            table {{
                width: 100%;
                max-width: 1000px;
                margin: auto;
                border-collapse: collapse;
                font-size: 22px;
            }}
            th, td {{
                border: 1px solid black;
                padding: 15px;
                text-align: center;
            }}
            th {{
                background-color: #ffcc99;
                font-weight: bold;
            }}
        </style>
    </head>
    <body>
        <h3>📌 최근 5경기 결과</h3>
        <table>
            <tr>
                <th>날짜</th>
                <th>홈팀</th>
                <th>스코어</th>
                <th>원정팀</th>
            </tr>
    """

    for match in past_matches:
        fixture = match["fixture"]
        teams = match["teams"]
        score = match["score"]
        html_content += f"""
            <tr>
                <td>{fixture['date'][:10]}</td>
                <td>{team_translation.get(teams['home']['name'], teams['home']['name'])}</td>
                <td>{score['fulltime']['home']} - {score['fulltime']['away']}</td>
                <td>{team_translation.get(teams['away']['name'], teams['away']['name'])}</td>
            </tr>
        """

    html_content += """
        </table>
        <h3>📌 향후 경기 일정</h3>
        <table>
            <tr>
                <th>날짜</th>
                <th>홈팀</th>
                <th>원정팀</th>
            </tr>
    """

    for match in future_matches:
        fixture = match["fixture"]
        teams = match["teams"]
        html_content += f"""
            <tr>
                <td>{fixture['date'][:10]}</td>
                <td>{team_translation.get(teams['home']['name'], teams['home']['name'])}</td>
                <td>{team_translation.get(teams['away']['name'], teams['away']['name'])}</td>
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
