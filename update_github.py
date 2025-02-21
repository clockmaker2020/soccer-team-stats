import os
import base64
import requests
from datetime import datetime

# ✅ GitHub 설정
GITHUB_USERNAME = "clockmaker2020"
GITHUB_REPO = "soccer-team-stats"
GITHUB_TOKEN = os.getenv("SOCCER_STATS_PAT")

if not GITHUB_TOKEN:
    print("❌ GitHub PAT가 설정되지 않았습니다. 환경 변수를 확인하세요.")
    exit(1)

# ✅ 데이터 폴더 생성 확인
TEAM_DATA_DIR = os.path.join(os.getcwd(), "data/team_data")
LEAGUE_FILE_PATH = os.path.join(os.getcwd(), "data/league_standings.json")
os.makedirs(TEAM_DATA_DIR, exist_ok=True)  # 디렉토리 강제 생성

# ✅ GitHub 업로드 함수
def upload_file(file_path, github_path, file_type):
    if not os.path.exists(file_path):
        print(f"⚠️ 파일 없음: {file_path}, 업로드 건너뜁니다.")
        return

    api_url = f"https://api.github.com/repos/{GITHUB_USERNAME}/{GITHUB_REPO}/contents/{github_path}"

    # ✅ 파일 읽기 및 인코딩
    with open(file_path, "rb") as file:
        encoded_file = base64.b64encode(file.read()).decode("utf-8")

    # ✅ 기존 파일 SHA 가져오기 (덮어쓰기)
    response = requests.get(api_url, headers={"Authorization": f"token {GITHUB_TOKEN}"})
    sha = response.json().get("sha") if response.status_code == 200 else None

    # ✅ GitHub API 요청 데이터 생성
    data = {
        "message": f"자동 업데이트 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ({file_type})",
        "content": encoded_file,
        "branch": "main"
    }
    if sha:
        data["sha"] = sha  

    # ✅ GitHub API 요청
    response = requests.put(api_url, json=data, headers={"Authorization": f"token {GITHUB_TOKEN}"})

    if response.status_code in [200, 201]:
        print(f"✅ GitHub에 {file_type} 업로드 완료: {file_path}")
    else:
        print(f"⚠️ 업로드 실패: {response.status_code} - {response.text}")

# ✅ `team_data` 폴더 내 모든 JSON 파일 업로드
for team_file in os.listdir(TEAM_DATA_DIR):
    if team_file.endswith(".json"):
        file_path = os.path.join(TEAM_DATA_DIR, team_file)
        github_path = f"data/team_data/{team_file}"
        upload_file(file_path, github_path, "팀별 JSON 데이터")

# ✅ 리그 순위 JSON 파일 업로드 (존재하는 경우)
if os.path.exists(LEAGUE_FILE_PATH):
    upload_file(LEAGUE_FILE_PATH, "data/league_standings.json", "리그 순위 데이터")
else:
    print("⚠️ 리그 순위 데이터 파일이 존재하지 않습니다. 업로드 건너뜁니다.")

print("🎉 모든 데이터 업로드 완료!")
