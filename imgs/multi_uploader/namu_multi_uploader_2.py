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
import csv
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
import os

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

def login_namu(driver, namu_id, namu_pw):     
    # 나무위키 로그인창 열기
    # redirect가 있어야 캡챠가 뚫리는듯 함
    driver.get("https://namu.wiki/member/login?")
    #sleep(3)
        
    # 사용자 ID 입력
    username_input = driver.find_element(By.NAME, "email")
    username_input.clear()
    username_input.send_keys(ID)

    # 비밀번호 입력
    password_input = driver.find_element(By.NAME, "password")
    password_input.clear()
    password_input.send_keys(PW)
        
    #login_button = driver.find_element(By.XPATH, "//button[contains(text(), '로그인')]")
    #login_button.click()
        
    # 캡챠 처리 대기 (수동)
    # 나무위키 로그인은 캡챠가 요구됨
    print("캡챠를 해결하고, 완료되면 터미널에서 'enter' 키를 누르세요.")
    input("")

    # 캡챠 처리 후 다음 단계로 진행
    print("캡챠가 해결되었습니다. 다음 작업을 시작합니다.")
    sleep(2)
    
def upload_image(driver, image_info):
    print('upload image', image_info[0])
    file_name = image_info[0]
    file_ref = image_info[1]
    
    try:
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
        # 첫결과 선택   : 433 364
        # 열기버튼      : 959 645
        pyautogui.moveTo(x=294, y=489)
        pyautogui.click()
        sleep(0.5)
            
        pyautogui.moveTo(x=920, y=257)
        pyautogui.click()
        pyperclip.copy(file_name)
        pyautogui.hotkey('command','v')
        sleep(0.5)
            
        pyautogui.moveTo(x=501, y=302)
        pyautogui.click()
        sleep(1)
            
        pyautogui.moveTo(x=433, y=364)
        pyautogui.click()
        sleep(1)
            
        pyautogui.moveTo(x=959, y=645)
        pyautogui.click()
        sleep(0.5)

        # 출처 입력
        source_input = driver.find_element(By.NAME, "text")
        if source_input is None:
            return False
        source_input.clear()
        source_input.send_keys(make_upload_detail(file_ref))

        # 라이선스 입력
        dropdown_menu = driver.find_elements(By.CLASS_NAME,"vs__dropdown-toggle")[0]
        if dropdown_menu is None:
            return False
        dropdown_menu.click()
        license_input = driver.find_element(By.ID,"licenseSelect")
        if license_input is None:
            return False
        license_input.click()
        license_input.send_keys('제한적 이용')
        license_input.send_keys(Keys.RETURN)
            
        # 분류 입력
        category_input = driver.find_element(By.ID, "categorySelect")
        if category_input is None:
            return False
        category_input.click()
        category_input.send_keys('포켓몬 카드 게임')
        category_input.send_keys(Keys.RETURN)

        ## 업로드 버튼 클릭
        #upload_button = driver.find_element(By.XPATH, "//button[contains(text(), '업로드')]")
        #if upload_button is None:
        #    print('button none')
        #    input()
        #    return False
        #print('button found')
        ##upload_button.click()
        #print('5초 안에 업로드 버튼을 눌러주세요')
        #sleep(5)
        #print('click upload')
        
        # 업로드 버튼 클릭
        pyautogui.scroll(-1000)
        pyautogui.moveTo(790,687)
        pyautogui.click()
        sleep(3)
        
        # 경고 창이 있는지 확인하고 처리
        handle_alert(driver)

        # 성공적으로 업로드 완료
        return True
    
    except Exception as e:
        print(f"Error occurred during upload: {e}")
        handle_alert(driver)
        return False

ID = 'yigunwoo97@gmail.com'
PW = '503d103H'

def upload_pokemon_imgs(poke_path):
    # Chrome for testing 위치 설정
    options = Options()
    options.binary_location = '/Users/lkw0127/chrome-mac-arm64/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing'
    
    # ChromeDriverManager를 사용하여 ChromeDriver 설치 및 경로 설정
    driver_path = "/Users/lkw0127/chromedriver-mac-arm64/chromedriver"
    service = Service(driver_path)
    driver = webdriver.Chrome(service=service, options=options)
    
    ref_path = poke_path + 'ref.csv'
    
    try:
        login_namu(driver, ID, PW)
        
        # CSV 파일을 읽고 한 줄씩 처리하면서 바로 저장하는 구조
        with open(ref_path, mode='r', newline='', encoding='utf-8') as read_file:
            reader = csv.reader(read_file)
            rows = list(reader)  # 전체 데이터를 메모리에 로드

        # CSV 파일을 다시 쓰기 모드로 열지 않고, 추가 모드로 열어서 한 줄씩 즉시 기록
        with open(ref_path, mode='r+', newline='', encoding='utf-8') as write_file:
            writer = csv.writer(write_file)

            for i, row in enumerate(rows):
                try:
                    print(i)
                    
                    # 이미 업로드한 이미지는 패스
                    if len(row) > 2 and row[2] == 'done':
                        continue

                    success = upload_image(driver, row)
                    
                    # 3번째 열에 "ok" 추가
                    if success:
                        print(f"{i} done")
                        if len(row) >= 3:  # 3번째 열이 존재하는지 확인
                            row[2] = "done"  # 3번째 열을 "ok"로 설정
                        else:
                            row.append("done")  # 3번째 열이 없다면 추가

                    # 처리된 행을 즉시 파일에 기록
                    writer.writerow(row)

                except Exception as e:
                    # 예외가 발생하면 에러 출력 및 행 처리 건너뜀
                    print(f"에러 발생: {e} - 데이터: {row}")
                    writer.writerow(row)  # 오류 발생해도 해당 행 기록
                    continue

    finally:
        print('quit!!')
        driver.quit()

# 포켓몬의 이미지가 들어있는 경로를 입력받고, 그 도감번호의 포켓몬 카드 이미지 전부 업로드
UPLOAD_POKEMON_PATH = '../pokemon/gen1/0020_레트라/'
if __name__ == '__main__':
    upload_pokemon_imgs(UPLOAD_POKEMON_PATH)