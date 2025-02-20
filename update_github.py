import os
import base64
import requests
from datetime import datetime

# ✅ GitHub 설정
GITHUB_USERNAME = "clockmaker2020"
GITHUB_REPO = "soccer-team-stats"
GITHUB_TOKEN = os.getenv("GITHUB_PAT_SOCCER_STATS")  # 환경 변수에서 PAT 가져오기

# ✅ 저장된 파일 가져오기 (이미지 + HTML)
IMAGE_DIR = "C:/Users/clock_p93/soccer-team-stats/images"
DATA_DIR = "C:/Users/clock_p93/soccer-team-stats/data"

# ✅ 업로드 대상 파일 리스트
image_files = [f for f in os.listdir(IMAGE_DIR) if f.endswith(".png")]
html_files = [f for f in os.listdir(DATA_DIR) if f.endswith(".html")]

# ✅ GitHub API 업로드 함수
def upload_file(file_path, github_path, file_type):
    api_url = f"https://api.github.com/repos/{GITHUB_USERNAME}/{GITHUB_REPO}/contents/{github_path}"

    # ✅ 파일 읽기 및 인코딩
    with open(file_path, "rb") as file:
        encoded_file = base64.b64encode(file.read()).decode("utf-8")

    # ✅ 기존 파일 SHA 가져오기 (덮어쓰기 위함)
    response = requests.get(api_url, headers={"Authorization": f"token {GITHUB_TOKEN}"})
    sha = response.json().get("sha") if response.status_code == 200 else None

    # ✅ GitHub API 요청 데이터 생성
    data = {
        "message": f"자동 업데이트 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ({file_type})",
        "content": encoded_file,
        "branch": "main"
    }
    if sha:
        data["sha"] = sha  # 기존 파일이 있다면 덮어쓰기

    # ✅ GitHub API 요청 (파일 업로드)
    response = requests.put(api_url, json=data, headers={"Authorization": f"token {GITHUB_TOKEN}"})

    if response.status_code in [200, 201]:
        print(f"✅ GitHub에 {file_type} 업로드 완료: {file_path}")
    else:
        print(f"⚠️ 업로드 실패 ({file_type}): {response.json()}")

# ✅ 저장된 모든 파일 업로드 실행
for image_file in image_files:
    file_path = os.path.join(IMAGE_DIR, image_file)
    upload_file(file_path, f"images/{image_file}", "이미지")

for html_file in html_files:
    file_path = os.path.join(DATA_DIR, html_file)
    upload_file(file_path, f"data/{html_file}", "HTML")
