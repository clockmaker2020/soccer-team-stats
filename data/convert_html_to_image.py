import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from PIL import Image

# ✅ 저장 경로 설정
DATA_DIR = os.path.join(os.getcwd(), "data")
IMAGE_DIR = os.path.join(os.getcwd(), "images")
os.makedirs(IMAGE_DIR, exist_ok=True)

# ✅ Selenium 브라우저 옵션 설정
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=1200x800")

# ✅ Selenium 실행
driver = webdriver.Chrome(options=chrome_options)

# ✅ 저장된 HTML 파일들을 변환
for file_name in os.listdir(DATA_DIR):
    if file_name.endswith(".html"):
        team_name = file_name.replace("update_stats_", "").replace(".html", "")
        file_path = os.path.join(DATA_DIR, file_name)

        # ✅ HTML 파일이 존재하는지 확인
        if not os.path.exists(file_path):
            print(f"⚠️ {team_name}의 HTML 파일이 없습니다. 변환을 건너뜁니다.")
            continue  # HTML이 없으면 변환하지 않음

        print(f"📌 {team_name} HTML을 이미지로 변환 중...")

        # ✅ HTML 파일 열기
        file_url = "file:///" + file_path.replace("\\", "/")
        driver.get(file_url)
        time.sleep(3)  # 페이지 로드 대기

        # ✅ 스크린샷 저장
        image_path = os.path.join(IMAGE_DIR, f"latest_result_{team_name}.png")
        driver.save_screenshot(image_path)

        # ✅ 이미지 크롭 (불필요한 여백 제거)
        image = Image.open(image_path)
        cropped_image = image.crop((0, 0, 1200, 800))  # 필요에 따라 조정
        cropped_image.save(image_path)

        print(f"✅ 이미지 변환 완료: {image_path}")

driver.quit()
print("🎉 모든 팀의 HTML을 이미지로 변환 완료!")
