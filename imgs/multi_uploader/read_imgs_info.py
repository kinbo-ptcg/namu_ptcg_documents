#imgs 파일의 모든 폴더, 파일 순회하면서 
#파일명, 타입, 시리즈 순서대로 csv출력

import os
import csv

if __name__ == "__main__":
    # 특정 폴더 경로
    folder_path = '../imgs/'
    csv_path = './local_imgs_info.csv'
    
    csv_data = []

    # 모든 파일에 접근하는 코드
    for dirpath, dirnames, filenames in os.walk(folder_path):
        for filename in filenames:
            # 각 파일의 전체 경로
            file_path = os.path.join(dirpath, filename)
            csv_data.append(file_path.split('/')[2:])
            
    # write csv
    with open(csv_path, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        for item in csv_data:
            writer.writerow(item)