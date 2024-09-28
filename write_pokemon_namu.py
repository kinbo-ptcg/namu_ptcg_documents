# 본 파일은 DB의 xxxx_name.json형식의 파일을 템플릿:포켓몬 카드 게임/카드 목록/포켓몬 형식으로 변환하는 것을 목표로 한다.
# 샘플로써 누오의 문서를 만들어보자
import json
import copy
import pprint
import os
from collections import Counter

#1: 양식 신경쓰지 말고 개별 카드의 틀이 잘 되었나 확인
#JSON_PATH = './0195_누오.json'
#2: 진화 확인
JSON_PATH = './jsons/0103_나시.json'
JSON_PATH = './jsons/버드렉스.json'
JSON_PATH = './jsons/펄기아.json'
#JSON_PATH = './jsons/제라오라.json'
JSON_PATH = './jsons/텅비드.json'
JSON_PATH = './jsons/매시붕.json'
JSON_PATH = './card_data/pokemon/gen2/0195_누오.json'

# 속성 심볼 크기
SYBL_BIG = 20
SYBL_SML = 17

# 색상코드
GRA_CODE = '#56AF58'
FIR_CODE = '#DA3642'
WAT_CODE = '#4FAFE6'
LIG_CODE = '#F8D648'
FIG_CODE = '#B76D3B'
PSY_CODE = '#9986BA'
DAR_CODE = '#3F7885'
MET_CODE = '#B7BAA9'
DRA_CODE = '#818D41'
COL_CODE = '#D6D5D8'
FAI_CODE = '#D5578A'

def get_color(poke_type):
    if '(풀)' in poke_type: return GRA_CODE
    elif '(불꽃)' in poke_type: return FIR_CODE
    elif '(물)' in poke_type: return WAT_CODE
    elif '(번개)' in poke_type: return LIG_CODE
    elif '(격투)' in poke_type: return FIG_CODE
    elif '(초)' in poke_type: return PSY_CODE
    elif '(악)' in poke_type: return DAR_CODE
    elif '(강철)' in poke_type: return MET_CODE
    elif '(드래곤)' in poke_type: return DRA_CODE
    elif '(무색)' in poke_type: return COL_CODE
    elif '(페어리)' in poke_type: return FAI_CODE
    else: return "#000000" # 시꺼먼게 출력되면 뭔가 문제가 있다는 의미

# "포켓몬"카드의 한국어 카드명과 포켓몬 정보를 받아서
# 일본어 카드명, 영어 카드명을 반환하는 코드
MULTILAN_PATH = './assets/pokemon_name_multilan.json'
def translate_poke_cardname(card_name_kr,pokemons_info):
    with open(MULTILAN_PATH,'r',encoding='utf-8') as f:
        data = json.load(f)
        
    # 뮤&뮤츠 가 Mew&Mew츠 로 번역되는 참사를 막기위해 pokemons_info를 포켓몬 이름길이순으로 소트
    pokemons_info = sorted(pokemons_info, key=lambda x: len(x["name"]))
    
    # 일본어 이름으로
    card_name_jp = card_name_kr
    for pokemon_info in pokemons_info:
        poke_name_kr = pokemon_info['name']
        poke_name_jp = data[pokemon_info["pokedexNumber"]-1]['jpn']
        card_name_jp = card_name_jp.replace(poke_name_kr,poke_name_jp)
        # 리전폼은 지역명 번역
        card_name_jp = card_name_jp.replace('알로라','アローラ')
        card_name_jp = card_name_jp.replace('가라르','ガラル')
        card_name_jp = card_name_jp.replace('히스이','ヒスイ')
        card_name_jp = card_name_jp.replace('팔데아','パルデア')
        # 특수 키워드
        card_name_jp = card_name_jp.replace('찬란한 ','かがやく')
        card_name_jp = card_name_jp.replace('빛나는 ','ひかる')
    
    # 엉문이름으로
    card_name_en = card_name_kr
    for pokemon_info in pokemons_info:
        poke_name_kr = pokemon_info['name']
        poke_name_en = data[pokemon_info["pokedexNumber"]-1]['eng']
        card_name_en = card_name_en.replace(poke_name_kr,poke_name_en)
        # 리전폼은 지역명 번역
        card_name_en = card_name_en.replace('알로라','Alola')
        card_name_en = card_name_en.replace('가라르','Galar')
        card_name_en = card_name_en.replace('히스이','Hisui')
        card_name_en = card_name_en.replace('팔데아','Paldea')
        # 특수 키워드
        card_name_en = card_name_en.replace('찬란한','Radiant')
        card_name_en = card_name_en.replace('빛나는','Shining')
        

    
    return card_name_jp, card_name_en

# 어느 포켓몬에서 진화했는지 알아내기
# 입력 : item
# 출력 : evo_text
# evo_text: 진화포켓몬이면 '~에서 진화', 기본포켓몬이면 ''출력
# 룰 : subtypes를 보고 어떤 규칙을 적용시킬지 판단
# M진화 : (이름에서 M땐것)에서 진화
# V진화 : (이름에서 MAX,STAR땐것)에서 진화
# 1진화,2진화 : evo_data에서 찾기
# 이외에서는 ''
import assets.evo_data as pokedex
def get_pokename_with_region(poke_info):
    poke_name = poke_info['name'].replace(' ','')
    poke_region = poke_info.get('region','')
    return poke_info.get('region','')+poke_info['name']

def get_evo_info(item):
    if '기본' in item['subtypes'] or '복원' in item['subtypes'] or 'V-UNION' in item['subtypes']:
        evo_text = ''
    else:
        if 'M진화' in item['subtypes']:
            evo_from = item['name'].replace('M','').strip()
        elif 'V진화' in item['subtypes']:
            evo_from = get_pokename_with_region(item['pokemons'][0]) + ' V'
        elif 'BREAK진화' in item['subtypes'] or '레벨업' in item['subtypes']:
            evo_from = get_pokename_with_region(item['pokemons'][0])
        elif '1진화' in item['subtypes'] or '2진화' in item['subtypes']:
            evo_from = pokedex.EVOLVED_FROM[item['pokemons'][0]['name']]
            
            if evo_from != '':
                name = evo_from
                region = item['pokemons'][0].get('region','')
                evo_from = get_pokename_with_region({'name':name,'region':region})
            else:
                # 화석포켓몬은 게임에선 1진화인데 카드에선 2진화이기때문에 처리필요
                evo_from='!화석포켓몬!카드확인!'
        evo_text = evo_from + '에서 진화'
    
    return evo_text

# 서브타입 디코드
SUBTYPES_PK_TAIL =[
    '기본',
    '1진화',
    '2진화',
    '복원'
]
SUBTYPES_PK_HEAD =[
    'EX',
    'GX',
    'V',
    'V-UNION',
    'VMAX',
    'VSTAR',
    'ex'
]
SUBTYPES_PK_NONE =[
    'BREAK진화',
    'M진화',
    'TAG TEAM',
    'V진화',
    '고대',
    '레벨업',
    '미래',
    '연격',
    '일격',
    '퓨전',
    '프리즘스타',
    '플라스마단',
    '찬란한'
]
SUBTYPES_NP_1 = [
    '기본 에너지',
    '특수 에너지',
    '서포트',
    '스타디움',
    '아이템',
    '포켓몬의 도구'
]
SUBTYPES_NP_2 = [
    'ACE SPEC',
    'TAG TEAM',
    '프리즘스타'
]
SUBTYPES_NP_3 = [
    '연격',
    '일격',
    '퓨전',
    '고대',
    '미래',
    '플라스마단',
    '플레어단 기어',
    '플레어단 하이퍼기어'
]

def get_subtype_script(supertype,subtypes):
    subtype_text = ""
    if supertype == "pk": #pk pokemon
        # ~~ 포켓몬
        for subtype in SUBTYPES_PK_TAIL:
            if subtype in subtypes:
                subtype_text += subtype + " 포켓몬 | "
        
        # 포켓몬 ~~
        for subtype in SUBTYPES_PK_HEAD:
            if subtype in subtypes:
                subtype_text += "포켓몬 " + subtype + " | "

        # ~~ 
        for subtype in SUBTYPES_PK_NONE:
            if subtype in subtypes:
                subtype_text += subtype + " | "  
    elif supertype == "np": #np none pokemon
        # 트레이너즈, 에너지 대분류
        for subtype in SUBTYPES_NP_1:
            if subtype in subtypes:
                subtype_text += subtype + " | "  
                
        # 에이스스펙, 태그팀, 프리즘스타
        for subtype in SUBTYPES_NP_2:
            if subtype in subtypes:
                subtype_text += subtype + " | "  
        
        # 기타 키워드
        for subtype in SUBTYPES_NP_3:
            if subtype in subtypes:
                subtype_text += subtype + " | "  
    else:
        subtype_text += "none"
        
    # 특정 키워드들은 아이콘으로 변환
    # 태그팀, 연격, 일격, 퓨전, 울트라비스트, 고대, 미래, 플라스마단
    if 'TAG TEAM' in subtypes:
        subtype_text = subtype_text.replace('TAG TEAM','[[파일:TAG TEAM.png|height=18px]]')
    if '연격' in subtypes:
        subtype_text = subtype_text.replace('연격','[[파일:연격.png|height=18px]]')
    if '일격' in subtypes:
        subtype_text = subtype_text.replace('일격','[[파일:일격.png|height=18px]]')
    if '퓨전' in subtypes:
        subtype_text = subtype_text.replace('일격','[[파일:퓨전_pk.png|height=18px]]')
    if '울트라비스트' in subtypes:
        subtype_text = subtype_text.replace('울트라비스트','[[파일:울트라비스트.png|height=18px]]')
    if '고대' in subtypes:
        subtype_text = subtype_text.replace('고대','[[파일:포케카 고대.png|height=18px]]')
    if '미래' in subtypes:
        subtype_text = subtype_text.replace('미래','[[파일:포케카 미래.png|height=18px]]')
    if '플라스마단' in subtypes:
        subtype_text = subtype_text.replace('플라스마단','[[파일:플라스마단.png|height=18px]]')
    
    return subtype_text[:-2] if len(subtype_text) >= 2 else subtype_text

# 카드 텍스트 안에 있는 (강철) 같은 것들을 
# [[파일:포켓몬 카드 게임 강철타입.png|width=18px]]
# 의 형식으로 변환
def type_text_to_symbol(text,size):
    text_cp = copy.deepcopy(text)
    
    text_cp = text_cp.replace('(풀)','[[파일:포켓몬 카드 게임 풀타입.png|width='+str(size)+'px]]')
    text_cp = text_cp.replace('(불꽃)','[[파일:포켓몬 카드 게임 불꽃타입.png|width='+str(size)+'px]]')
    text_cp = text_cp.replace('(물)','[[파일:포켓몬 카드 게임 물타입.png|width='+str(size)+'px]]')
    text_cp = text_cp.replace('(번개)','[[파일:포켓몬 카드 게임 번개타입.png|width='+str(size)+'px]]')
    text_cp = text_cp.replace('(격투)','[[파일:포켓몬 카드 게임 격투타입.png|width='+str(size)+'px]]')
    text_cp = text_cp.replace('(초)','[[파일:포켓몬 카드 게임 초타입.png|width='+str(size)+'px]]')
    text_cp = text_cp.replace('(악)','[[파일:포켓몬 카드 게임 악타입.png|width='+str(size)+'px]]')
    text_cp = text_cp.replace('(강철)','[[파일:포켓몬 카드 게임 강철타입.png|width='+str(size)+'px]]')
    text_cp = text_cp.replace('(드래곤)','[[파일:포켓몬 카드 게임 드래곤타입.png|width='+str(size)+'px]]')
    text_cp = text_cp.replace('(무색)','[[파일:포켓몬 카드 게임 무색타입.png|width='+str(size)+'px]]')
    text_cp = text_cp.replace('(페어리)','[[파일:포켓몬 카드 게임 페어리타입.png|width='+str(size)+'px]]')
    text_cp = text_cp.replace('(0코)','[[파일:포켓몬 카드 게임 0코스트.png|width='+str(size)+'px]]')
    text_cp = text_cp.replace('(플러스)','[[파일:포켓몬 카드 게임 플러스.png|width='+str(size)+'px]]')

    return text_cp

# 룰 텍스트를 
# ex 룰 : 사이드 두장 어쩌고
# 의 양식으로 반환하는 함수
# item['subtypes']에서 추출
def get_rules_script(item):
    subtypes = item['subtypes']
    
    # BREAK, V-UNION, 레벨업처리
    if "BREAK진화" in subtypes:
        return "BREAK진화 : " + item['rules'][0] + "\n"
    if "V-UNION" in subtypes:
        return "V-UNION 룰 : " + item['rules'][0] + "포켓몬 V-UNION이 기절한 경우 상대는 프라이즈를 3장 가져간다.\n"
    if "레벨업" in subtypes:
        return "레벨업 : " + item['rules'][0] + "\n"
    
    rules_script = ""
    # M진화, 테라스탈, 아르세우스 룰, 프리즘스타 룰,찬란한 룰 처리
    if 'M진화' in subtypes:
        rules_script += "M진화 : M진화 포켓몬으로 진화하면 자신의 차례는 끝난다.\n"
    if '테라스탈' in subtypes:
        rules_script += "테라스탈 : 이 포켓몬은 벤치에 있는 한, 기술의 데미지를 받지 않는다.\n"
    if '아르세우스' in subtypes:
        rules_script += "아르세우스 룰 : 이 카드는 덱에 몇 장이라도 넣을 수 있다.\n"
    if '프리즘스타' in subtypes:
        rules_script += "프리즘스타	룰 : 같은 이름의 ◇ (프리즘스타) 의 카드는 덱에 1장만 넣을 수 있다. 트래쉬가 아닌 로스트존에 둔다.\n"
    if '찬란한' in subtypes:
        rules_script += "찬란한 룰 : 찬란한 포켓몬은 덱에 1장만 넣을 수 있다.\n"
        
    # TAG TEAM ,EX, GX, VMAX, VSTAR, V, ex
    if 'TAG TEAM' in subtypes:
        rules_script += "TAG TEAM 룰 : TAG TEAM이 기절한 경우 상대는 프라이즈를 3장 가져간다.\n"
    if 'EX' in subtypes:
        rules_script += "EX 룰 : 포켓몬 EX가 기절한 경우 상대는 프라이즈를 2장 가져간다.\n"
    if 'GX' in subtypes:
        rules_script += "GX 룰 : 포켓몬 GX가 기절한 경우 상대는 프라이즈를 2장 가져간다.\n"
    if 'VMAX' in subtypes:
        rules_script += "VMAX 룰 : 포켓몬 VMAX가 기절한 경우 상대는 프라이즈를 3장 가져간다.\n"
    if 'VSTAR' in subtypes:
        rules_script += "VSTAR 룰 : 포켓몬 VSTAR가 기절한 경우 상대는 프라이즈를 2장 가져간다.\n"
    if 'V' in subtypes:
        rules_script += "V 룰 : 포켓몬 V가 기절한 경우 상대는 프라이즈를 2장 가져간다.\n"
    if 'ex' in subtypes:
        rules_script += "ex 룰	포켓몬 ex가 기절한 경우 상대는 프라이즈를 2장 가져간다.\n"
        
    return rules_script

# EX,BREAK,GX,V,VMAX,VSTAR,ex,프리즘스타 를 아이콘으로 표시하기
def get_card_name(item):
    name = item['name']
    if 'EX' in name:
        name = name.replace('EX','[[파일:포케카 EX.png|height=18px]]')
        if 'M' in name:
            return name.replace('M','[[파일:M_pkc.png|height=18px]]')
        else:
            return name
    elif 'BREAK' in name:
        return name.replace('BREAK','[[파일:포케카 BREAK.png|height=18px]]')
    elif 'GX' in name:
        if '울트라비스트' in item['subtypes']:
            if '&' in name:
                return name.replace('GX','[[파일:포케카 GXREDTT.png|height=18px]]')
            else:
                return name.replace('GX','[[파일:포케카 GXRED.png|height=18px]]')
        elif '&' in name:
            return name.replace('GX','[[파일:포케카 GXTT.png|height=18px]]')
        else:
            return name.replace('GX','[[파일:포케카 GX.png|height=18px]]')
    elif 'V' in name:
        if '레벨업' in item['subtypes']:
            return name
        elif 'VSTAR' in name:
            return name.replace('VSTAR','[[파일:포케카 VSTAR.png|height=18px]]')
        elif 'VMAX' in name:
            return name.replace('VMAX','[[파일:포케카 VMAX.png|height=18px]]')
        else:
            return name.replace('V','[[파일:포케카 V.png|height=18px]]')
    elif 'ex' in name:
        if '테라스탈' in item['subtypes']:
            return name.replace('ex','[[파일:포케카 ex_tera.png|height=18px]]')
        else:
            return name.replace('ex','[[파일:포케카 ex.png|height=18px]]')
    elif '◇' in name:
        return name.replace('◇','[[파일:프리즘스타.png|height=18px]]')
    else:
        return name
    
# 카드 한장의 데이터를 템플릿:포켓몬 카드 게임/카드 로 변환
def write_card(item):
    #결과를 저장하는 텍스트
    card_script = ""
    
    #이름 직전부분
    template_head = """
{{{{{{#!wiki style="width:100%; border:2px solid #000000; background:{card_color}; color:#000;"
{{{{{{#!wiki style="margin:0; padding:8px; color: #fff"
{{{{{{#!wiki style="font-size:1.2em;"    
"""
    #색상 결정
    poke_type = item['type']
    card_color = get_color(poke_type)
    
    card_script += template_head.format(card_color=card_color)
    
    #맨 윗줄. 이름 3개국어, 체력, 타입, 진화정보
    template_top = """'''{card_name_kr}'''{{{{{{#!wiki style="font-size:1.0em;float:right"
HP {hp} {poke_type}
}}}}}}}}}}}}{{{{{{#!wiki style="font-size:1.0em;"
{card_name_jp}{{{{{{#!wiki style="float:right;"
{evol_from}
}}}}}}}}}}}}{card_name_en}
"""
    card_name_kr = get_card_name(item)
    card_name_jp, card_name_en = translate_poke_cardname(item['name'],item['pokemons'])
    hp = str(item['hp'])
    poke_type_symbol = type_text_to_symbol("".join(item['type']),SYBL_BIG)
    evol_from = get_evo_info(item)
    
    card_script += template_top.format(card_name_kr=card_name_kr, hp = hp, poke_type=poke_type_symbol, card_name_jp=card_name_jp, evol_from=evol_from,card_name_en=card_name_en)
    
    # 포켓몬의 유형이 들어오는 진한칸
    template_mid = """}}}}}}{{{{{{#!wiki style="width:auto; margin:0px 5px 5px 5px; border-radius:5px; padding:4px; background:#00000077; color:#fff"
{subtypes} 
"""
    subtypes = get_subtype_script("pk",item['subtypes'])
    
    card_script += template_mid.format(subtypes=subtypes)
    
    # 특성, 기술, 플레이버텍스트 순으로 들어오는 연한칸
    card_text  = """}}}{{{#!wiki style="width:auto%; margin:0px 5px 0px 5px; padding: 4px; border-radius: 5px; word-break: keep-all; background:#ffffffdd;"   
"""
    template_bot_abil = """{{{{{{#red  {abil_type} '''{abil_name}'''}}}}}}
{abil_text}
"""
    template_bot_attack = """{attack_cost} '''{attack_name}''' {attack_damage}
{attack_text}
"""
    template_bot_vanilla_attack = """{attack_cost} '''{attack_name}''' {attack_damage}
"""

    template_bot_flavor = """{{{{{{#!wiki style="border-top: .0625rem solid #000; margin: 5px 0 5px 0" 
}}}}}}{{{{{{-2 ''{flavor_text}''}}}}}} 
"""

    # 특성, 고대능력, 포켓파워, 포켓바디 라면, 각각에 맞춘 디자인에 따라서 어빌리티를 표현하기
    if item['abilities']:
        for ability in item['abilities']:
            if ability.get('special') == 'VSTAR':
                continue
            else:
                card_text += template_bot_abil.format(abil_type=ability['type'],abil_name=ability['name'],abil_text=ability['text']).replace('특성','[[파일:포케카 특성.png|height=18px]]').replace('포켓바디','[[파일:포켓바디.png|height=18px]]').replace('포켓파워','[[파일:포켓파워.png|height=18px]]')
    
    # 공격 출력
    # VSTAR, GX 기술은 따로 표현하기
    if item['attacks']:
        for attack in item['attacks']:
            if attack.get('special','') in ['VSTAR','GX']:
                continue
            elif attack['text']:
                card_text += template_bot_attack.format(attack_cost = attack['cost'],attack_name=attack['name'],attack_damage=attack['damage'],attack_text=attack['text'])
            else:
                card_text += template_bot_vanilla_attack.format(attack_cost = attack['cost'],attack_name=attack['name'],attack_damage=attack['damage'])
                
    card_text=card_text.rstrip('\n')
                
    # VSTAR파워 출력. 이건 특성 or 공격
    if 'VSTAR' in item['subtypes']:
        # VSTAR 구분선
        card_text += """}}}{{{#!wiki style="text-align: center; width:auto%; margin:0px 5px 0px 5px; padding: 4px; border-radius: 5px; word-break: keep-all; background: linear-gradient(180deg, #f7e330, #f3f5fb 50%, #b6a406); color: #7F6317; text-shadow: #FFFFFF 1px 2px 2px;"
'''VSTAR 파워'''}}}{{{#!wiki style="width:auto%; margin:0px 5px 0px 5px; padding: 4px; border-radius: 5px; word-break: keep-all; background:#ffffffdd;"
"""

        vstar_done = False
        for ability in item['abilities']:
            if ability.get('special') == 'VSTAR':
                vstar_done = True
                card_text += template_bot_abil.format(abil_type=ability['type'],abil_name=ability['name'],abil_text=ability['text']).replace('특성','[[파일:포케카 특성.png|height=18px]]')
                
        if not vstar_done:
            for attack in item['attacks']:
                if attack.get('special','') == 'GX':
                    card_text += template_bot_attack.format(attack_cost = attack['cost'],attack_name=attack['name'],attack_damage=attack['damage'],attack_text=attack['text'])
    # GX기술 출력
    if 'GX' in item['subtypes'] or 'TAG TEAM' in item['subtypes']:
        gx_template = """}}}}}}{{{{{{#!wiki style="width:auto%; margin:0px 5px 0px 5px; padding: 4px; border-radius: 5px; word-break: keep-all; background: linear-gradient(135deg, #00aadd, #000024); color: #FFF;;"
{attack_cost} '''{attack_name}''' {attack_damage}
{attack_text}"""
        for attack in item['attacks']:
            if attack.get('special','') == 'GX':
                if '울트라비스트' in item['subtypes']:
                    card_text += gx_template.format(attack_cost = attack['cost'],attack_name=attack['name'],attack_damage=attack['damage'],attack_text=attack['text']).replace('linear-gradient(135deg, #00aadd, #000024)','linear-gradient(45deg, #d03620, #0a0000)')
                else:
                    card_text += gx_template.format(attack_cost = attack['cost'],attack_name=attack['name'],attack_damage=attack['damage'],attack_text=attack['text'])
                break

    if item['flavorText']:
        card_text += template_bot_flavor.format(flavor_text=item['flavorText'].replace('\n',' '))
        
    # card_text에 있는 타입마크 ( (불꽃) 등 ) 을 이미지로 변환
    card_text = type_text_to_symbol(card_text,SYBL_SML)
    card_script += card_text
    
    # 약점, 저항력, 후퇴부분
    template_tail = """}}}}}}{{{{{{#!wiki style="margin:0; padding:8px; color: #fff"
약점 : '' {weakness} '' | 저항력 : '' {resistance} '' | 후퇴 : '' {retreat} ''    
"""
    # 약점
    if item['weakness']['type'] == "":
        weakness = "--"
    else:
        weakness = type_text_to_symbol(item['weakness']['type'],SYBL_BIG) + ' ' +  item['weakness']['value']
        
    # 저항력
    if item['resistance']['type'] == "":
        resistance = "--"
    else:
        resistance = type_text_to_symbol(item['resistance']['type'],SYBL_BIG) + ' ' +  item['resistance']['value']
        
    # 후퇴
    if item['retreatCost'] == 0:
        retreat = "--"
    else:
        retreat = ""
        for _ in range(item['retreatCost']):
            retreat += "[[파일:포켓몬 카드 게임 무색타입.png|width=20px]] "
            
    card_script += template_tail.format(weakness=weakness,resistance=resistance,retreat=retreat)
    
    # 룰
    template_tail_rule = """{{{{{{#!wiki style="border-top: .0625rem solid #000; margin: 5px 0 5px 0" 
}}}}}}{rules}
"""
    if item['rules']:
        rules = get_rules_script(item)
        card_script += template_tail_rule.format(rules=rules)
        
    template_tail_final = """}}}}}}     
"""

    card_script += template_tail_final
    
    return card_script

REGULATION_ORDER = [
    'H','G','F','E','D','C','B','A',
    'XY','BW','DP',
    'ADV-PCG', 'e', 'Neo', '오리지널']    

from collections import defaultdict
from datetime import datetime
import csv

PROD_CSV = './prod_info.csv'
def get_data_namu(data):
    # release-date 획득
    # csv_data[i][4,8,1] = [db상의 이름, 나무위키에서 이름, 한국발매일]
    csv_data = {}
    with open(PROD_CSV, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file,delimiter=',')
        for row in reader:
            if row[0] != '':
                if row[8] == '': namu_name = row[4]
                else: namu_name = row[8]
                csv_data[row[4]] = {'namu': namu_name,'release-date':row[1]}
        
    for item in data:
        for version_info in item['version_infos']:
            try:
                version_info['release_date'] = datetime.strptime(csv_data.get(version_info['prodName'], {'release-date': '2099/12/31', 'namu': 'unknown'})['release-date'], '%Y/%m/%d')
            except ValueError:
                version_info['release_date'] = datetime(2099, 12, 31)  # 기본값 설정
                
            version_info['namu_docu_name'] = csv_data.get(version_info['prodName'], {'namu': 'unknown'})['namu']
        
        item['version_infos'].sort(key=lambda x: x['release_date'])
        item['first_release_date'] = item['version_infos'][0]['release_date']
        item['first_prodName'] = item['version_infos'][0]['namu_docu_name']
    
    # regulation 값으로 그룹화
    grouped_data = {}
    for item in data:
        regu = min(item['regulationMark'], key=lambda x: REGULATION_ORDER.index(x))
        if regu not in grouped_data:
            grouped_data[regu] = []
        grouped_data[regu].append(item)
        
    # 각 그룹 내에서 release-date(발매일)로 정렬
    for reg, items in grouped_data.items():
        grouped_data[reg] = sorted(items, key=lambda x: x['first_release_date'])
        
    # regulation을 역순으로 정렬
    grouped_data = dict(sorted(grouped_data.items(), key=lambda x: REGULATION_ORDER.index(x[0])))

    return grouped_data

import pokedex_ptcg_kr
POKEDEX_FIRST = 1
POKEDEX_LAST = 1025
ORDER_TLE_NAME = '포켓몬 카드 일람'

def to_four_digit(num):
    if num < 10:
        return '000' + str(num)
    elif num < 100:
        return '00' + str(num)
    elif num < 1000:
        return '0' + str(num)
    else:
        return str(num)

def write_order_table(data):
    def get_pokemon_name(pokedex_num):
        # 값과 키를 뒤집은 새로운 사전 생성
        POKEDEX_REVERSED = {value: key for key, value in pokedex_ptcg_kr.POKEDEX.items()}
        return POKEDEX_REVERSED.get(pokedex_num, "포켓몬이 존재하지 않습니다")
    
    template = """
||<-5><tablealign=center><tablewidth=900><tablebordercolor=#ddd,#383b40><bgcolor=#ddd,#1f2023><tablebgcolor=#fff,#2d2f34><tablecolor=#373a3c,#ddd><height=32> '''포켓몬 카드 게임의 포켓몬 카드일람''' ||
||<width=30%> {before} || {{{{{{+1 →}}}}}} ||<width=30%><bgcolor=#f5f5f5,#191919><color=#2e2e2e,#ddd> '''{now}''' || {{{{{{+1 →}}}}}} ||<width=30%> {after} ||
"""
    cell_template = "[[파일:icon{pokedex_num}_f00_s0.png|width=40]] {pokedex_num} [[{pokemon_name}/포켓몬 카드 게임|{pokemon_name}]]"
    pokedex_num = data[0]['pokemons'][0]["pokedexNumber"]
    pokemon_name = data[0]['pokemons'][0]["name"]
    if pokedex_num == POKEDEX_FIRST:
        before = ''
        now = cell_template.format(pokedex_num=to_four_digit(pokedex_num),pokemon_name=pokemon_name)
        after = cell_template.format(pokedex_num=to_four_digit(pokedex_num+1),pokemon_name=get_pokemon_name(pokedex_num+1))
    elif pokedex_num == POKEDEX_LAST:
        before = cell_template.format(pokedex_num=to_four_digit(pokedex_num-1),pokemon_name=get_pokemon_name(pokedex_num-1))
        now = cell_template.format(pokedex_num=to_four_digit(pokedex_num),pokemon_name=pokemon_name)
        after = ''
    else:
        before = cell_template.format(pokedex_num=to_four_digit(pokedex_num-1),pokemon_name=get_pokemon_name(pokedex_num-1))
        now = cell_template.format(pokedex_num=to_four_digit(pokedex_num),pokemon_name=pokemon_name)
        after = cell_template.format(pokedex_num=to_four_digit(pokedex_num+1),pokemon_name=get_pokemon_name(pokedex_num+1))    
    
    return template.format(before=before, now=now, after=after)

def write_header(data):
    header_template = """[include(틀:포켓몬 카드 게임/레귤레이션)]
[include(틀:포켓몬 카드 게임/카드일람)]
{card_order_tle}
[목차]
[clearfix]

== 개요 ==
[[포켓몬 카드 게임]]의 포켓몬 카드.
## 포켓몬의 설명을 기술부탁드립니다.  
"""
    
    return header_template.format(card_order_tle = write_order_table(data))


REGULATION_ORDER = [
    'H','G','F','E','D','C','B','A',
    'XY','BW','DP',
    'ADV-PCG', 'e', 'Neo', '오리지널']   
def write_regu_title(regu):
    if regu in ['H','G','F','E','D','C','B','A']:
        return f"== {regu} 레귤레이션 ==\n"
    elif regu in ['XY','BW','DP', 'ADV-PCG', 'e', 'Neo', '오리지널']:
        return f"== {regu} 시리즈 ==\n"
    
def write_prod_title(prod_name):
    return f"=== [[{prod_name}]] ===\n"

def write_card_title(card_name):
    return f"==== {card_name} ====\n"

def cardUrl_to_name(url):
    return url.split('/')[-1].replace('?w=512','').strip()

LOW_RARITY_ORDER = {'N':0, 'C':1, 'U':2, 'R':3, 'RR':4, 'RRR':5}

# 최초수록 최소레어 카드의 이미지명, 레어도를 출력
def find_main_img_detail(version_infos, product):
    first_infos = []
    
    # namu_docu_name이 product와 일치하는 카드정보를 모으기
    for info in version_infos:
        if info['namu_docu_name'] == product:
            first_infos.append(info)
            
    # fisrt_infos에서 가장 레어도가 낮은걸 찾기
    if len(first_infos)==1:
        return cardUrl_to_name(first_infos[0]['cardImgURL']), first_infos[0]['rarity']
    else:
        lowest_rarity_url = ''
        lowest_rarity = ''
        lowest_rarity_num = 100
        for info in first_infos:
            if lowest_rarity_num > LOW_RARITY_ORDER.get(info['rarity'],50):
                lowest_rarity = info['rarity']
                lowest_rarity_num = LOW_RARITY_ORDER.get(info['rarity'],50)
                lowest_rarity_url = info['cardImgURL']
        
        return cardUrl_to_name(lowest_rarity_url), lowest_rarity
    
def write_card_main_img_table(item):
        
    img_table_template = """||<tablealign=center><rowbgcolor=#ffffff><width=512px> [[파일:{img_name}|width=100%]] ||
|| [[{product}]][br][include(틀:포케카 레어도/{rarity})] ||
"""
#||<tablealign=center><rowbgcolor=#ffffff><width=100%> [[파일:SV6_033.png|width=100%]]||
#|| [[변환의 가면]][br][include(틀:포케카 레어도/R)] ||
    product = item['first_prodName']
    img_name, rarity = find_main_img_detail(item['version_infos'],product)

    return img_table_template.format(img_name = img_name, product = product, rarity= rarity)

def write_card_other_img_table(item):
    infos = item['version_infos']
    
    # 만약 version_infos가 길이1이라면 아무것도 출력하지 않기
    if len(infos) == 1:
        return ''
    
    # 다른 일러스트 들어가는 표
    tabke_script = "## 이 표는 DB에 따라 기계적으로 채워진 것입니다. 직접 이미지를 확인하시고 중복된 이미지를 셀채로 삭제바랍니다."
    table_script = "{{{#!folding [ 다른 일러스트 보기 ]\n"
    
    # 최초수록,최소레어를 제외한 'version_infos' 만을 사용
    main_img_name, main_img_rarity = find_main_img_detail(infos,item['first_prodName'])
    other_img_infos = []
    for info in infos:
        if info['rarity'] == main_img_rarity and cardUrl_to_name(info['cardImgURL']) == main_img_name:
            continue
        other_img_infos.append(info)
        
    # other_img_infos가 하나뿐이라면 1x1인 표 사용
    # 아니라면 2열짜리 표 사용
    # 순서는 발매일이 빠른게 앞으로 오고, 카드번호가 빠른게 앞으로 오도록
    if len(other_img_infos)==1:
        img_name = cardUrl_to_name(other_img_infos[0]['cardImgURL'])
        product = other_img_infos[0]['namu_docu_name']
        rarity = other_img_infos[0]['rarity']
        table_script += f"||<tablealign=center><rowbgcolor=#ffffff><width=100%> [[파일:{img_name}|width=512px]] ||\n"
        table_script += f"|| [[{product}]][br][include(틀:포케카 레어도/{rarity})] ||\n"
        table_script += "}}}\n"
        return table_script
    else:
        # 'release-date'와 'number' 순으로 정렬
        other_img_infos = sorted(other_img_infos, key=lambda x: (x['release_date'], int(x['number'])))

        # 두 개씩 처리
        i = 0
        while i < len(other_img_infos) - 1:
            info_left = other_img_infos[i]
            info_right = other_img_infos[i + 1]

            # 두 개를 묶어서 처리하는 부분
            img_left = cardUrl_to_name(info_left['cardImgURL'])
            img_right = cardUrl_to_name(info_right['cardImgURL'])
            product_left = info_left['namu_docu_name']
            product_right = info_right['namu_docu_name']
            rarity_left = info_left['rarity']
            rarity_right = info_right['rarity']
            if i == 0:
                table_script += f"||<tablealign=center><rowbgcolor=#ffffff><width=50%> [[파일:{img_left}|width=100%]] ||<width=50%> [[파일:{img_right}|width=100%]]||\n"
            else:
                table_script += f"||<rowbgcolor=#ffffff><width=50%> [[파일:{img_left}|width=100%]] ||<width=50%> [[파일:{img_right}|width=100%]] ||\n"
            table_script += f"|| [[{product_left}]][br][include(틀:포케카 레어도/{rarity_left})] || [[{product_right}]][br][include(틀:포케카 레어도/{rarity_right})] ||\n"

            i += 2  # 두 개씩 건너뛰기

        # 만약 하나만 남았다면 예외 처리
        if i == len(other_img_infos) - 1:
            info_last = other_img_infos[i]
            img_last = cardUrl_to_name(info_last['cardImgURL'])
            product_last = info_last['namu_docu_name']
            rarity_last = info_last['rarity']
            
            table_script += f"||<rowbgcolor=#ffffff> [[파일:{img_last}|width=100%]] ||\n"
            table_script += f"|| [[{product_last}]][br][include(틀:포케카 레어도/{rarity_last})] ||\n"
            
        table_script += "}}}\n"
        return table_script

REGUS = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N']
def write_card_release_table(item):
    release_table = "||<tablewidth=100%><tablebordercolor=#000000><tablebgcolor=#fff,#191919><bgcolor=#777777><color=#fff>수록 정보 ||\n"

    release_infos = sorted(item['version_infos'],key=lambda x: (x['release_date'], int(x['number'])))
    for info in release_infos:
        regu = info['regu']
        
        symbol_name = info['prodSymbolURL'].split('/')[-1]
        head, tail = os.path.splitext(symbol_name)
        symbol = head.upper() + tail
    
        num = info['number'] + '/' + info['prodNumber']
        prod_name = info['namu_docu_name']
        rarity = info['rarity']
        
        release_table += "||[include(틀:국기, 국명=대한민국, 출력= )] |"
        if regu in REGUS:
            release_table += f" [[파일:regu_{regu}.png|height=25]] |"
        release_table += f" [[파일:{symbol}|height=25]] |"
        release_table += f" {num} |"
        release_table += f" [[{prod_name}]]"
        if rarity != "N":
            release_table += f" | [include(틀:포케카 레어도/{rarity})]"
        release_table += " ||\n"
        
    return release_table

def write_card_section(item):
    card_section = ""
    
    # 카드 대표이미지 표 작성
    # 일단 "최초 수록 제품의 최저레어도" 이미지만 넣고,
    # 나중에 수동으로 "다른제품에 최저레어도 다른 일러스트" 이미지도 넣기
    card_section += write_card_main_img_table(item)
    
    # 카드 텍스트 작성
    card_section += write_card(item)
    
    # 다른 일러스트 펼쳐보기
    card_section += write_card_other_img_table(item)
    
    # 유저가 작성한 카드 설명이 들어가는 부분
    card_section += "## 유저가 작성하는 카드 설명이 들어가는 부분입니다.\n"
    
    # 수록정보 표 작성
    card_section += write_card_release_table(item)
    
    return card_section

# 도감번호에서 세대 구하기
# 멜탄, 멜메탈은 7세대로 분류
GEN1 = 151  #뮤
GEN2 = 251  #세레비
GEN3 = 386  #테오키스
GEN4 = 493  #아르세우스
GEN5 = 649  #게노세크트
GEN6 = 721  #볼케니온
GEN7 = 809  #멜메탈
GEN8 = 905  #러브로스
GEN9 = 1025 #복숭악동
def get_pokedex_gen(num):
    GEN_NUMS = [0,GEN1,GEN2,GEN3,GEN4,GEN5,GEN6,GEN7,GEN8,GEN9]
    for gen in range(1,len(GEN_NUMS)):
        if num <= GEN_NUMS[gen]:
            return gen
    print('Invalid Pokedex number')
    return 0

def write_pokemon_docu(data):
    data_namu = get_data_namu(data)
        
    #나무위키 문서 본문
    namu_script = ''  
    
    # 헤더 : 틀, 목차 및 개요문단
    namu_script += write_header(data)
    
    # 본문 : 레귤레이션별 카드 목록문단
    for regu in REGULATION_ORDER:
        if regu in data_namu:
            namu_script += write_regu_title(regu)
            i = 0
            while i < len(data_namu[regu]):
                item = data_namu[regu][i]

                # 다음 아이템과 비교
                match_count = 1
                while (i + match_count < len(data_namu[regu]) and
                       data_namu[regu][i + match_count]['first_prodName'] == item['first_prodName']):
                    match_count += 1

                # 제품명을 추가
                namu_script += write_prod_title(item['first_prodName'])

                # 만약 여러 개가 일치한다면 한 번에 처리
                if match_count > 1:
                    for j in range(i,i+match_count):
                        item_match = data_namu[regu][j]
                        namu_script += write_card_title(item_match['name'])
                        # 카드 설명 문단 작성
                        namu_script += write_card_section(item_match)
                    i += match_count  # 일치하는 만큼 건너뜀
                else:
                    # 카드 설명 문단 작성
                    namu_script += write_card_section(item)
                    i += 1

    # 풋터 : 분류 및 문서가져오기 문단
    namu_script += "[clearfix]\n"
    # 세대 틀
    gen_list = []
    for item in data:
        for pokemon in item['pokemons']:
            gen_list.append(get_pokedex_gen(pokemon['pokedexNumber']))
            
    gen_counter = Counter(gen_list)
    gen, _ = gen_counter.most_common(1)[0]
    
    namu_script += f"[[분류:포켓몬 카드 게임/{gen}세대]]"
    
    # 타입 틀
    type_list = []
    for item in data:
        type_list.append(item['type'].replace('(','').replace(')','').strip())
    
    type_counter = Counter(type_list)
    type_common = type_counter.most_common()
    
    for type_, _ in type_common:
        namu_script += f"[[분류:포켓몬 카드 게임/{type_} 타입]]"
    
    # 문서가져오기 꼭 넣기!!
    namu_script += "\n## 만약 다른 문서에서 내용을 일부 가져오셨다면, 문서 가져옴 틀을 꼭 넣어주세요"
    
    return namu_script

POKE_ROOT = './card_data/pokemon/'
def write_pokemon_namu_all():
    base_directory = POKE_ROOT
    save_root = './poke_namu/'

    # 하위 폴더를 포함하여 모든 JSON 파일에 접근
    for root, dirs, files in os.walk(base_directory):
        for file in files:
            if file.endswith('.json'):
                file_path = os.path.join(root, file)
                try:
                    save_path = save_root + file_path.split('/')[-2] + '/' + file_path.split('/')[-1]
                    save_path = save_path.replace('json','namu')
                    print(save_path)
                    
                    if not os.path.exists(os.path.dirname(save_path)):
                        os.makedirs(os.path.dirname(save_path))
                        
                    with open(file_path, 'r', encoding='utf-8') as json_file:
                        data = json.load(json_file)
                    namu_script = write_pokemon_docu(data)
                    
                    with open(save_path,'w',encoding='utf-8') as file:
                        file.write(namu_script)
                    
                except Exception as e:
                    print(f"Error processing {file_path}: {e}")

if __name__ == "__main__":
    write_pokemon_namu_all()
        
    