import re
from urllib.parse import urlparse
import requests
import os
import json
import pandas as pd

def get_card_img(url, card_img_path,error_log_file):
    try:
        card_img_url = url
        card_img_file_name = urlparse(card_img_url).path.split('/')[-1]
        card_img_file_path = os.path.join(card_img_path, card_img_file_name)
                
        if not os.path.exists(card_img_path):
            os.makedirs(card_img_path)
            
        # 파일이 이미 존재하는지 확인
        if os.path.exists(card_img_file_path):
            print(f"File already exists, skipping download: {card_img_file_name}")
            return
        
        # 이미지 저장
        img_res = requests.get(url)
        img_res.raise_for_status()  # 요청이 성공했는지 확인

        with open(card_img_file_path, 'wb') as f:
            f.write(img_res.content)

        print(f"Image downloaded and saved successfully: {card_img_file_name}")

    except Exception as e:
        # 예외가 발생한 URL을 외부 파일에 기록
        with open(error_log_file, 'a') as log_file:
            log_file.write(f"Failed to download {url}: {str(e)}\n")
        print(f"Failed to download {url}: {str(e)}")

if __name__ == "__main__":    
    gens = [1,2,3,4,5,6,7,8,9]
    poke_data_dir = '../card_data/pokemon/gen'
    
    #다운로드 하기 전에 전체 이미지수 카운트
    img_count_total = 0
    for gen in gens:
        root_dir = poke_data_dir + str(gen)+ '/'
        for root, dirs, files in os.walk(root_dir):
            for file in files:
                if file.endswith('.json'):
                    file_path = os.path.join(root, file)
                    with open(file_path, 'r', encoding='utf-8') as json_file:
                        data = json.load(json_file)
                        for item in data:
                            for item_ver in item['version_infos']:
                                img_count_total += 1
    
    # 이미지 다운로드, 업로드때 필요한 엑셀 생성
    img_count = 0
    for gen in gens:
        root_dir = poke_data_dir + str(gen)+ '/'
        log_file = './error_log_gen'+str(gen)+'.txt'
        for root, dirs, files in os.walk(root_dir):
            for file in files:
                if file.endswith('.json'):
                    file_path = os.path.join(root, file)
                    with open(file_path, 'r', encoding='utf-8') as json_file:
                        data = json.load(json_file)
                        img_dir = './pokemon/gen' +str(gen) + '/' + file.replace('.json','')
                        reference_list = []
                        #print(file_path)
                        for item in data:
                            for item_ver in item['version_infos']:
                                img_count += 1
                                #print(f"{img_count}/{img_count_total} : {file}")
                                imgURL = item_ver['cardImgURL']
                                #get_card_img(imgURL,img_dir,log_file)
                                reference_list.append([imgURL.split('/')[-1].replace('?w=512',''),imgURL])
                                
                        if '파이리' in file_path:
                            print(reference_list)
                        df = pd.DataFrame(reference_list)
                        os.makedirs(os.path.dirname(img_dir + '/ref.csv'), exist_ok=True)
                        df.to_csv(img_dir + '/ref.csv',index=False, header=False, encoding='utf-8-sig')
                                
                                
                                
                                
                        
        
