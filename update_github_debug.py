import os
import requests

# ✅ GitHub Personal Access Token 확인
GITHUB_TOKEN = os.getenv("SOCCER_STATS_PAT")
if not GITHUB_TOKEN:
    print("❌ [ERROR] 환경 변수 SOCCER_STATS_PAT가 설정되지 않았습니다!")
    exit(1)
else:
    print(f"✅ [INFO] GitHub Access Token 감지됨 (길이: {len(GITHUB_TOKEN)})")

# ✅ GitHub API 테스트 요청
api_test_url = "https://api.github.com/user"
headers = {"Authorization": f"token {GITHUB_TOKEN}"}
response = requests.get(api_test_url, headers=headers)

print(f"✅ [TEST] GitHub API 응답 상태 코드: {response.status_code}")
print(f"✅ [TEST] GitHub API 응답 데이터: {response.json()}")
