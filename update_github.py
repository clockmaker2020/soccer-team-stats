import os
import json
from datetime import datetime
from github import Github

# ✅ GitHub 인증 정보 (PAT 사용)
GITHUB_TOKEN = os.getenv("SOCCER_STATS_PAT")  # GitHub Secrets에서 PAT 가져오기
REPO_NAME = "clockmaker2020/soccer-team-stats"
DATA_DIR = os.path.join(os.getcwd(), "data")
POST_DATA_FILE = os.path.join(DATA_DIR, "post_data.json")

# ✅ GitHub 인증 및 저장소 접근
g = Github(GITHUB_TOKEN)
repo = g.get_repo(REPO_NAME)

# ✅ 업데이트할 파일 리스트
files_to_update = [POST_DATA_FILE]

# ✅ GitHub에 파일 업데이트 함수
def update_file_on_github(file_path, commit_message):
    try:
        file_name = os.path.basename(file_path)
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()

        # ✅ GitHub에서 기존 파일 정보 가져오기
        file_in_repo = repo.get_contents(f"data/{file_name}")

        # ✅ 변경된 내용이 있을 때만 업데이트
        if file_in_repo.decoded_content.decode("utf-8") != content:
            repo.update_file(
                file_in_repo.path, commit_message, content, file_in_repo.sha, branch="main"
            )
            print(f"✅ GitHub 업데이트 완료: {file_name}")
        else:
            print(f"🔄 변경 사항 없음: {file_name}")

    except Exception as e:
        print(f"⚠️ [ERROR] {file_name} 업데이트 실패: {e}")

# ✅ 모든 파일 업데이트 실행
for file in files_to_update:
    if os.path.exists(file):
        update_file_on_github(file, f"Update {os.path.basename(file)} - {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')}")

print("🎉 GitHub 데이터 업데이트 완료!")
