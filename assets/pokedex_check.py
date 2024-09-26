# pokemon_name_multilan.json과 pokedex_ptcg_kr.py의 한국어 포켓몬 이름이 일치하는지 확인
# pokedex_ptcg_kr.py 는 몇번이고 확인한것이므로 믿어도 됨

import json

import pokedex_ptcg_kr
TARGET_PATH = './pokemon_name_multilan.json'

if __name__ == "__main__":
    pokedex = pokedex_ptcg_kr.POKEDEX
    
    with open(TARGET_PATH,'r',encoding='utf-8') as f:
        data = json.load(f)
        
    name_kr_lst = list(pokedex.keys())
        
    for num in range(1025):
        name_kr = name_kr_lst[num]
        check_kr = data[num]['kor']
        
        if name_kr != check_kr:
            print(name_kr," : ",check_kr," <-")