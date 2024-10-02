# 나무위키에 이미지 하나하나 업로드 하는게 너무 힘들다
# 그걸 Selenium.ChromeDriver을 이용해서 자동화 해본다.
# 이미지업로드에 필요한 정보는
# 1. 이미지 절대경로
# 2. 나무위키에 업로드될 이미지의 이름
# 3. 출처 url
# 4. 라이선스종류(대부분 제한적 이용)
# 5. 분류
# 이렇게 다섯가지를 인자로 받는 업로드 함수를 만들어보자

import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep
from webdriver_manager.chrome import ChromeDriverManager
import pyautogui
import pyperclip
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.alert import Alert
from selenium.common.exceptions import UnexpectedAlertPresentException, NoAlertPresentException, TimeoutException

def wait_for_element(driver, by, value, timeout=10):
    try:
        element = WebDriverWait(driver, timeout).until(EC.presence_of_element_located((by, value)))
        return element
    except TimeoutException:
        print(f"Timeout while waiting for element {value}")
        handle_alert(driver)
        return None


def handle_alert(driver):
    try:
        alert = Alert(driver)
        print(f"Alert detected: {alert.text}")
        alert.accept()  # 경고 창을 확인하고 닫음
    except NoAlertPresentException:
        pass  # 경고 창이 없는 경우 아무 작업도 하지 않음


def make_upload_detail(source):
    text_base = '''
[목차]
== 기본 정보 ==
|| 출처 || {source} ||
|| 날짜 || 이미지가 만들어진 날짜를 삽입해 주세요. ||
|| 저작자 || 이미지의 저작자를 삽입해 주세요. ||
|| 저작권 || 이미지의 저작권과 관련된 기타 정보를 삽입해 주세요. ||
|| 기타 || 기타 정보가 있으면 삽입해 주세요. ||

== 이미지 설명 ==
이미지의 자세한 설명을 적어 주세요.
'''
    return text_base.format(source=source)

def login_namu(namu_id, namu_pw):     
    # 나무위키 로그인창 열기
    # redirect가 있어야 캡챠가 뚫리는듯 함
    driver.get("https://namu.wiki/member/login?redirect=%2Fw%2F%25EB%2582%2598%25EB%25AC%25B4%25EC%259C%2584%25ED%2582%25A4%3A%25EB%258C%2580%25EB%25AC%25B8")
    #sleep(3)
        
    # 사용자 ID 입력
    username_input = driver.find_element(By.NAME, "email")
    username_input.clear()
    username_input.send_keys(ID)

    # 비밀번호 입력
    password_input = driver.find_element(By.NAME, "password")
    password_input.clear()
    password_input.send_keys(PW)
        
    login_button = driver.find_element(By.XPATH, "//button[contains(text(), '로그인')]")
    login_button.click()
        
    # 캡챠 처리 대기 (수동)
    # 나무위키 로그인은 캡챠가 요구됨
    print("캡챠를 해결하고, 완료되면 터미널에서 'enter' 키를 누르세요.")
    input("")

    # 캡챠 처리 후 다음 단계로 진행
    print("캡챠가 해결되었습니다. 다음 작업을 시작합니다.")
    sleep(3)

ID = 'yigunwoo97@gmail.com'
PW = '503d103H'
UPLOAD_DATA = './prod_code/SV.json'

if __name__ == '__main__':
    
    # Chrome for testing 위치 설정
    options = Options()
    options.binary_location = '/Users/lkw0127/chrome-mac-arm64/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing'
    
    # ChromeDriverManager를 사용하여 ChromeDriver 설치 및 경로 설정
    driver_path = "/Users/lkw0127/chromedriver-mac-arm64/chromedriver"
    service = Service(driver_path)
    driver = webdriver.Chrome(service=service, options=options)

    try:
        login_namu(ID,PW)
        
        # JSON 파일 로드
        with open(UPLOAD_DATA, 'r') as f:
            images_info = json.load(f)
            
        # Namuwiki 이미지 업로드 페이지로 이동
        #driver.get("https://namu.wiki/Upload")
        
        for image_info in images_info:
            # 새로운 이미지 업로드를 위해 업로드 페이지로 이동
            print('goto upload page')
            driver.get("https://namu.wiki/Upload")
            print('in upload page')
            
            # 파일 선택 버튼 클릭
            wait_for_element(driver, By.XPATH, "//button[text()='Select']")
            select_button = driver.find_element(By.XPATH, "//button[text()='Select']")
            select_button.click()
            sleep(1)  # 파일 선택 창이 열리는 시간을 고려한 짧은 대기

            # PyAutoGUI를 이용하여 Finder에서 파일 선택
            # 단말마다 좌표가 다르니 적절히 찾을것
            # 폴더 쇼트컷   : 294 489
            # 검색창 클릭   : 920 257
            # 검색 폴더 선택 : 501 302
            # 첫결과 선택   : 430 364
            # 열기버튼      : 959 645
            pyautogui.moveTo(x=294, y=489)
            pyautogui.click()
            sleep(1)
            
            pyautogui.moveTo(x=920, y=257)
            pyautogui.click()
            pyperclip.copy(image_info['file_name'].split('.')[0].replace('&',' ').replace('「',' ').replace( '」',' ').replace('_',' '))
            pyautogui.hotkey('command','v')
            sleep(1)
            
            pyautogui.moveTo(x=501, y=302)
            pyautogui.click()
            sleep(1)
            
            pyautogui.moveTo(x=430, y=384)
            pyautogui.click()
            sleep(1)
            
            pyautogui.moveTo(x=959, y=645)
            pyautogui.click()
            sleep(1)
            
            sleep(1)
            # 우선 계속 대기(1000초 등)로 하고, 파일 하나 검색, 선택하는지 얼마나 걸리는지 확인하기
            
            # 업로드명 입력
            #upload_name_input = driver.find_element(By.NAME, "document")
            #upload_name_input.clear()
            #upload_name_input.send_keys(image_info['namu_img_name'])

            # 출처 입력
            source_input = driver.find_element(By.NAME, "text")
            source_input.clear()
            source_input.send_keys(make_upload_detail(image_info['source']))

            # 라이선스 입력
            dropdown_menu = driver.find_elements(By.CLASS_NAME,"vs__dropdown-toggle")[0]
            dropdown_menu.click()
            license_input = driver.find_element(By.ID,"licenseSelect")
            license_input.click()
            license_input.send_keys(image_info['license'])
            license_input.send_keys(Keys.RETURN)
            
            # 분류 입력
            category_input = driver.find_element(By.ID, "categorySelect")
            category_input.click()
            category_input.send_keys(image_info['category'])
            category_input.send_keys(Keys.RETURN)

            # 업로드 버튼 클릭
            upload_button = driver.find_element(By.XPATH, "//button[contains(text(), '업로드')]")
            upload_button.click()
            print('click upload')
            
            # 경고 창이 있는지 확인하고 처리
            handle_alert(driver)
            print('no alert')

            # 업로드 완료 후 다음 이미지 업로드를 위한 페이지 로딩 대기
            wait_for_element(driver, By.XPATH, "//button[text()='Select']")
            print('wait end')

    except UnexpectedAlertPresentException:
        handle_alert(driver)
        print('yes alert')
        
    finally:
        # WebDriver 종료
        driver.quit()

