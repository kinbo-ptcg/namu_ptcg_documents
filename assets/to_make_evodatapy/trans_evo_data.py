# 목표 : 각 포켓몬의 진화전 포켓몬을 알고싶다
import json
import pokedex_ptcg_kr
# 진화데이터 evo_data.json을 다음과 같이 변환
# 1: no, name, form, isMegaEvo, evolve_to 만 남기자
# 2: 메가진화 삭제 (나중에 메가진화는 따로처리)
# 3: no match 처리
# 4: 메가진화 키 삭제
# 5: no가 같으면 form이 달라도 evolve_to가 같은가 -> 같다
#    form키 삭제
# 6: evolve_from 추가후 evolve_to에서 evolve_from 내용생성
# 7: evolve_from, evolve_to가 모순이 없는지 확인
# 8: 8,9세대 포켓몬 데이터만 추가해두기, evlove_to,from = [-1]
# 9: 진화전 포켓몬 이름을 적은 딕셔너리를 파이썬 파일로 분리해서 import할수 있도록 하기
#    evolve_from['님피아'] = '이브이' 처럼
STEP = 9

JSON_PATH = './evo_data.json'

def trans_jp_to_kr(name_jp):
    with open('./pokemon_name_multilan.json','r',encoding='utf-8') as f:
        data= json.load(f)
        
    for item in data:
        if name_jp == item['jpn']:
            return item['kor']
        
    return 'no match'

if __name__ == "__main__":
    with open(JSON_PATH,'r',encoding='utf-8') as f:
        data = json.load(f)
        
    if STEP == 1:
        json_data = []
        for item in data:
            json_data.append({
                'no' : item['no'],
                'name' : trans_jp_to_kr(item['name']),
                'form' : item['form'],
                'isMega' : item['isMegaEvolution'],
                'evolve_to' : item['evolutions']
            })
        
        with open(JSON_PATH,'w',encoding='utf-8') as file:
            json.dump(json_data, file, indent=4, ensure_ascii=False)
    elif STEP == 2:
        json_data = []
        for item in data:
            if not item['isMega']:
                json_data.append(item)
                
        with open(JSON_PATH,'w',encoding='utf-8') as file:
            json.dump(json_data, file, indent=4, ensure_ascii=False)
    elif STEP == 3:
        for item in data:
            if item['name'] == "no match":
                print(item)    
    elif STEP == 4:
        json_data = []
        for item in data:
            json_data.append({
                "no": item['no'],
                "name": item['name'],
                "form": item['form'],
                "evolve_to": item['evolve_to']
            })
        with open(JSON_PATH,'w',encoding='utf-8') as file:
            json.dump(json_data, file, indent=4, ensure_ascii=False)
    elif STEP == 5:
        json_data = []
        for i in range(1,len(data)):
            if data[i]['no'] != data[i-1]['no']:
                item = data[i]
                json_data.append({
                    "no": item['no'],
                    "name": item['name'],
                    "evolve_to": item['evolve_to']
                })
        with open('./test.json','w',encoding='utf-8') as file:
            json.dump(json_data, file, indent=4, ensure_ascii=False)
    elif STEP == 6:   
        json_data = []
        for item in data:
            json_data.append({
                "no": item['no'],
                "name": item['name'],
                "evolve_to": item['evolve_to'],
                "evolve_from": []
            })
        
        for item in json_data:
            for evolve_num in item['evolve_to']:
                json_data[evolve_num-1]['evolve_from'].append(item['no'])
                
            print(item)
        
        with open("evo_data_test.json",'w',encoding='utf-8') as file:
            json.dump(json_data, file, indent=4, ensure_ascii=False)
    elif STEP == 7:
        with open("./evo_data.json",'r',encoding='utf-8') as f:
            data= json.load(f)
            
        for item in data:
            for evolve_num in item['evolve_to']:
                if item['no'] not in data[evolve_num-1]['evolve_from']:
                    print('bubu')
                    print(item)
    elif STEP == 8:
        name_list = []
        for item in data:
            name_list.append(item['name'])
            
        for poke_name in pokedex_ptcg_kr.POKEDEX:
            if poke_name not in name_list:
                data.append({
                    "no": pokedex_ptcg_kr.POKEDEX[poke_name],
                    "name": poke_name,
                    "evolve_to": [-1],
                    "evolve_from": [-1]
                })
                
        with open(JSON_PATH,'w',encoding='utf-8') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
    elif STEP == 9:
        evolved_from = {}
        for item in data:
            if item['evolve_from']:
                evolved_from[item['name']] = data[item['evolve_from'][0]-1]['name']
            else:
                evolved_from[item['name']] = ''
            
        print(evolved_from)
## 끝!!!!!