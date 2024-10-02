from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

if __name__ == '__main__':
    options = Options()
    options.binary_location = '/Users/lkw0127/chrome-mac-arm64/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing'

    # ChromeDriverManager를 사용하여 ChromeDriver 설치 및 경로 설정
    service = Service(ChromeDriverManager().install())

    driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.get("https://www.google.com")
        print(driver.title)
    finally:
        driver.quit()
