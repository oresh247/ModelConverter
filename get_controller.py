# coding:utf-8
import json
import os

dir_root =r'C:\_GITLAB\modelconverter' # корневой каталог
dir_rest_controllers_name = dir_root + r'\paths' # каталог обработки файлов схем рест контроллеров

def add_path(key,val):
    global controllers
    controllers[list(val[list(val.keys())[0]]['tags'])[0]]['paths'][key]=val


with open('apidocs.json', encoding='utf-8') as fh:
    controllers_json = json.load(fh)


controllers = {v['name']:{'tags':[v], 'paths': {}} for v in controllers_json['tags']}
for k, v in controllers_json['paths'].items(): add_path(k, v)


for k, v in controllers.items():
    with open(dir_rest_controllers_name+"\\"+f"{k}.json", 'w', encoding='utf-8') as outfile:
        json.dump(v, outfile, indent=2, ensure_ascii=False)




