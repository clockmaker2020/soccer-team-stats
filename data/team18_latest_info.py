import os
import json
import requests
import time
import unicodedata
from datetime import datetime

# ✅ API 설정
API_KEY = "0776a35eb1067086efe59bb7f93c6498"
LEAGUE_ID = 78  # 분데스리가 ID
SEASON = 2024  # 최신 시즌
HEADERS = {"x-apisports-key": API_KEY}

# ✅ 저장 폴더 설정
SAVE_DIR = os.path.join(os.getcwd(), "data/team_data")
os.makedirs(SAVE_DIR, exist_ok=True)

# ✅ 팀명 입력 (정확한 API 표기 사용)
TARGET_TEAM = "Bayern München"  # API에서 사용되는 공식 팀명

# ✅ UTC 시간을 KST(한국 시간)으로 변환하는 함수 추가
def convertToKST(utc_date):
    date = datetime.strptime(utc_date, "%Y-%m-%dT%H:%M:%S%z")
    kst_date = date.astimezone().strftime("%Y-%m-%d %H:%M")  # ✅ KST 변환
    return kst_date

# ✅ API 요청 함수 (요청 제한 초과 시 처리 추가)
def fetch_data(url, retries=3):
    for attempt in range(retries):
        try:
            response = requests.get(url, headers=HEADERS, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            print(f"🔍 API 응답 데이터: {json.dumps(data, indent=2, ensure_ascii=False)}")  # API 응답 확인
            
            if "errors" in data and "requests" in data["errors"]:
                print("🚨 [ERROR] API 요청 제한 초과! 기존 데이터를 사용합니다.")
                return None
            
            return data.get("response", [])
        except requests.exceptions.RequestException as e:
            print(f"⚠️ [ERROR] API 요청 오류 (시도 {attempt+1}/{retries}): {e}")
            time.sleep(3)
    return None

# ✅ 1부 리그 팀 검색 후 특정 팀의 ID 찾기
def get_team_id(team_name):
    url = f"https://v3.football.api-sports.io/standings?league={LEAGUE_ID}&season={SEASON}"
    data = fetch_data(url)
    
    if not data:
        print("⚠️ [ERROR] API 요청 제한으로 인해 팀 ID를 가져올 수 없습니다.")
        return None
    
    if data:
        for team in data[0]["league"]["standings"][0]:
            normalized_team_name = unicodedata.normalize('NFC', team["team"]["name"])
            if normalized_team_name.lower() == team_name.lower():
                return team["team"]["id"]
    return None

# ✅ 특정 팀 ID 가져오기
team_id = get_team_id(TARGET_TEAM)
if not team_id:
    print(f"🚨 [ERROR] {TARGET_TEAM}의 팀 ID를 찾을 수 없습니다. 올바른 팀명을 사용했는지 확인하세요.")
    exit()

print(f"📌 {TARGET_TEAM} ({team_id}) 데이터 가져오는 중...")

# ✅ JSON 캐시 파일 경로
file_path = os.path.join(SAVE_DIR, f"{TARGET_TEAM.replace(' ', '_').lower()}_latest.json")

# ✅ 기존 JSON 데이터가 있으면 사용
if os.path.exists(file_path):
    print("📢 기존 JSON 데이터가 존재합니다. API 요청 없이 사용합니다.")
    with open(file_path, "r", encoding="utf-8") as file:
        latest_match_data = json.load(file)
else:
    print("📢 새로운 데이터를 가져옵니다.")
    latest_match_url = f"https://v3.football.api-sports.io/fixtures?team={team_id}&season={SEASON}&league={LEAGUE_ID}&status=FT&last=1"
    match_data = fetch_data(latest_match_url)
    
    if not match_data or len(match_data) == 0:
        print("🚨 [ERROR] API 응답에 경기 데이터가 없습니다. 최신 경기 데이터를 가져올 수 없습니다.")
        print(f"🔍 API 응답 내용: {match_data}")  # API 응답 확인
        exit()
    
    match = match_data[0]
    fixture_date_kst = convertToKST(match["fixture"]["date"])
    
    fixture_id = match["fixture"]["id"]
    fixture_detail_url = f"https://v3.football.api-sports.io/fixtures?id={fixture_id}"
    fixture_detail = fetch_data(fixture_detail_url)
    
    if not fixture_detail or len(fixture_detail) == 0:
        print("🚨 [ERROR] 경기 상세 데이터를 가져올 수 없습니다.")
        exit()
    
    fixture_detail = fixture_detail[0]
    
    stadium = fixture_detail.get("fixture", {}).get("venue", {}).get("name", "미정")
    referee = fixture_detail.get("fixture", {}).get("referee", "정보 없음")
    league_round = fixture_detail.get("league", {}).get("round", "라운드 정보 없음")
    
    latest_match_data = {
        "team": TARGET_TEAM,
        "date": fixture_date_kst,
        "stadium": stadium,
        "referee": referee,
        "league_round": league_round,
    }
    
    # ✅ JSON 저장
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(latest_match_data, file, indent=4, ensure_ascii=False)
    print(f"✅ {TARGET_TEAM} 경기 JSON 저장 완료! ({file_path})")
