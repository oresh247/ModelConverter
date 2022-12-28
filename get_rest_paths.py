# coding:utf-8
import json
import os

dir_root =r'C:\_GITLAB\modelconverter' # корневой каталог
dir_rest_schemes_name = dir_root + r'\paths\schemes' # каталог обработки файлов схем рест запросов
refNodes = ['$ref'] # блоки, где ссылки
refs = list()


def check(k, v, targetkey):
    global refs
    if k in targetkey: refs.append(str.split(v,'/')[-1])
    return k in targetkey


# Отбираем $ref
def get_ref(d, targetkey):
    if not isinstance(d, (dict, list)): return d
    elif isinstance(d, list): return [v for v in (get_ref(v, targetkey) for v in d)]
    else: return {k: v for k, v in ((k, get_ref(v, targetkey)) for k, v in d.items()) if check(k, v, targetkey)}


with open('apidocs.json', encoding='utf-8') as fh:
    definitions_json = json.load(fh)

get_ref(definitions_json['paths'], refNodes)
definitions = {k:v for k, v in definitions_json['definitions'].items() if k in refs}

for k, v in definitions.items():
    with open(dir_rest_schemes_name+"\\"+f"{k}.json", 'w', encoding='utf-8') as outfile:
        json.dump(v, outfile, indent=2, ensure_ascii=False)

