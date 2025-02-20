import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from PIL import Image

# ✅ 경로 설정
DATA_DIR = os.path.abspath("C:/Users/clock_p93/soccer-team-stats/data")
IMAGE_DIR = os.path.abspath("C:/Users/clock_p93/soccer-team-stats/images")

# ✅ 이미지 저장 폴더 생성 (없으면 자동 생성)
if not os.path.exists(IMAGE_DIR):
    os.makedirs(IMAGE_DIR)

# ✅ Selenium 브라우저 옵션 설정
chrome_options = Options()
chrome_options.add_argument("--headless")  # GUI 없이 실행
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=1200x800")

# ✅ HTML을 이미지로 변환하는 함수
def convert_to_image(html_path, team_name):
    driver = webdriver.Chrome(options=chrome_options)

    # ✅ HTML 파일 경로 수정 (Windows 경로 문제 해결)
    file_url = "file:///" + html_path.replace("\\", "/")
    driver.get(file_url)
    time.sleep(3)  # 페이지 로드 대기

    # ✅ 전체 페이지 스크린샷 저장
    screenshot_path = os.path.join(IMAGE_DIR, f"latest_result_{team_name}.png")
    driver.save_screenshot(screenshot_path)
    driver.quit()

    # ✅ 이미지 크롭 (불필요한 여백 제거)
    image = Image.open(screenshot_path)
    cropped_image = image.crop((0, 0, 1200, 800))  # 필요에 따라 조정
    cropped_image.save(screenshot_path)

    print(f"✅ 이미지 변환 완료: {screenshot_path}")

# ✅ 저장된 모든 HTML 파일을 변환 (모든 팀 처리)
for html_file in os.listdir(DATA_DIR):
    if html_file.startswith("update_stats_") and html_file.endswith(".html"):
        team_name = html_file.replace("update_stats_", "").replace(".html", "")
        convert_to_image(os.path.join(DATA_DIR, html_file), team_name)

print("🎉 모든 팀의 HTML을 이미지로 변환 완료!")
