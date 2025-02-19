import os
import base64
import requests
from datetime import datetime

# ✅ GitHub 설정
GITHUB_USERNAME = "clockmaker2020"
GITHUB_REPO = "soccer-team-stats"
GITHUB_TOKEN = os.getenv("GITHUB_PAT_SOCCER_STATS")  # 환경 변수에서 PAT 가져오기

# ✅ 저장된 이미지 파일 가져오기
IMAGE_DIR = "C:/Users/clock_p93/soccer-team-stats/images"
image_files = [f for f in os.listdir(IMAGE_DIR) if f.startswith("latest_result_") and f.endswith(".png")]

# ✅ GitHub API 업로드 함수
def upload_image(image_path, team_name):
    github_file_path = f"images/{os.path.basename(image_path)}"
    api_url = f"https://api.github.com/repos/{GITHUB_USERNAME}/{GITHUB_REPO}/contents/{github_file_path}"

    # ✅ 파일 읽기 및 인코딩
    with open(image_path, "rb") as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode("utf-8")

    # ✅ 현재 파일 SHA 값 가져오기 (기존 파일이 있다면 덮어쓰기 위함)
    response = requests.get(api_url, headers={"Authorization": f"token {GITHUB_TOKEN}"})
    sha = response.json().get("sha") if response.status_code == 200 else None

    # ✅ GitHub API 요청 데이터 생성
    data = {
        "message": f"자동 업데이트 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ({team_name})",
        "content": encoded_image,
        "branch": "main"
    }
    if sha:
        data["sha"] = sha  # 기존 파일이 있다면 덮어쓰기

    # ✅ GitHub API 요청 (파일 업로드)
    response = requests.put(api_url, json=data, headers={"Authorization": f"token {GITHUB_TOKEN}"})

    if response.status_code in [200, 201]:
        print(f"✅ GitHub에 이미지 업로드 완료: {image_path}")
    else:
        print(f"⚠️ 업로드 실패 ({team_name}): {response.json()}")

# ✅ 저장된 모든 팀의 이미지 업로드 실행
for image_file in image_files:
    team_name = image_file.replace("latest_result_", "").replace(".png", "")
    image_path = os.path.join(IMAGE_DIR, image_file)
    upload_image(image_path, team_name)
