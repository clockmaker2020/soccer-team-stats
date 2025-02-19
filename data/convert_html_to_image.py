import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from PIL import Image

# ✅ 설정할 팀 이름
TEAM_NAME = "bayern"  # 바이에른 이외의 팀도 처리 가능하도록 변수 설정

# ✅ 기본 저장 경로 설정
BASE_DIR = "C:/Users/clock_p93/soccer-team-stats"
HTML_FILE = os.path.join(BASE_DIR, "data", f"update_stats_{TEAM_NAME}.html")
IMAGE_DIR = os.path.join(BASE_DIR, "images")
IMAGE_PATH = os.path.join(IMAGE_DIR, f"latest_result_{TEAM_NAME}.png")

# ✅ 이미지 저장 폴더 생성 (없으면 자동 생성)
if not os.path.exists(IMAGE_DIR):
    os.makedirs(IMAGE_DIR)

# ✅ Selenium 브라우저 옵션 설정
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=1200x800")

# ✅ Selenium 실행
driver = webdriver.Chrome(options=chrome_options)
file_url = f"file:///{HTML_FILE.replace('\\', '/')}"
driver.get(file_url)
time.sleep(3)  # 페이지 로드 대기

# ✅ 전체 페이지 스크린샷 저장
screenshot_path = os.path.join(IMAGE_DIR, f"temp_screenshot_{TEAM_NAME}.png")
driver.save_screenshot(screenshot_path)
driver.quit()

# ✅ 이미지 크롭 (불필요한 여백 제거)
image = Image.open(screenshot_path)
cropped_image = image.crop((0, 0, 1200, 800))  # 필요에 따라 조정
cropped_image.save(IMAGE_PATH)

print(f"✅ 이미지 변환 완료: {IMAGE_PATH}")
