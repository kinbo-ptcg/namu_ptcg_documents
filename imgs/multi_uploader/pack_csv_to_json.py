import csv
import json

CSV_PATH = './s_decks.csv'
OUT_JSON = './s_decks_img.json'

if __name__ == "__main__":
    data = []
    
    # CSV 파일 열기
    with open(CSV_PATH, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file,delimiter='\t')
        for row in reader:
            if row[0] != '':
                data.append(row[0:3])
                
    json_data = []
    
    for item in data:
        json_item = {}
        
        json_item['file_name'] = item[0]
        json_item['namu_img_name'] = '파일:' + item[1]
        json_item['source'] = item[2]
        json_item['license'] =  '제한적 이용'
        json_item['category'] = '포켓몬 카드 게임'
        
        json_data.append(json_item)
        
    with open(OUT_JSON,'w',encoding='utf-8') as file:
        json.dump(json_data, file, indent=4, ensure_ascii=False)