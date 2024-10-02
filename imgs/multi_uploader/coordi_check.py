import pyautogui
import time

if __name__ == '__main__':
    print('start')
    while True:
        x, y = pyautogui.position()
        print(f"X: {x} Y: {y}")
    
        time.sleep(1.0)
        
# 로그인 버튼 누르기
# 유저버튼      : 1190 279
# 로그인버튼    : 1034 559
        
# 첫 시도  
# 폴더 쇼트컷   : 294 489
# 검색창 클릭   : 920 257
# 검색 폴더 선택 : 501 302
# 첫결과 선택   : 430 364
# 열기버튼      : 959 645