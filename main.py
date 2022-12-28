# coding:utf-8
import json
import os

# глобальные переменные
delNodes = ['$schema', '$comment','dependencies'] # удаляемые блоки
refNodes = ['$ref'] # блоки, где меняем ссылки
dir_root =r'C:\_GITLAB\modelconverter' # корневой каталог
dir_schemes_name = dir_root + r'\definitions' # каталог обработки файлов схем модели
dir_rest_schemes_name = dir_root + r'\paths\schemes' # каталог обработки файлов схем рест запросов
dir_rest_controllers_name = dir_root + r'\paths' # каталог обработки файлов схем рест контроллеров
dir_dto_map = dir_root + r'\map' # Каталог расположения файлов мапинга
file_name_header = 'header.json' # Файл с заголовком для модели SWAGGER
file_name_model = 'model.json' # Генерируемый файл итоговой модели
file_name_dto_map_key = 'dtomapkey.json'  # Замена самих названий ДТО
file_name_dto_map_val = 'dtomapval.json'  # Замена названий в ссылках на ДТО (иногда надо заменить только ссылки без замены названия ДТО)
postfix = 'Dto' # Добавляется к названию схемы (так сейчас сделано в разработке)


# Удаление объектов по ключу
def remove_key(d, targetkey):
    if not isinstance(d, (dict, list)): return d
    elif isinstance(d, list): return [v for v in (remove_key(v, targetkey) for v in d)]
    else: return {k: v for k, v in ((k, remove_key(v, targetkey)) for k, v in d.items()) if k not in targetkey}


# Мапинг ДТО ключей
def map_key(d, targetkey):
    if not isinstance(d, (dict, list)): return d
    elif isinstance(d, list): return [v for v in (map_key(v, targetkey) for v in d)]
    else: return {targetkey.get(k) if k in targetkey else k : v for k, v in ((k, map_key(v, targetkey)) for k, v in d.items())}

# Мапинг ДТО значений (ссылок)
def map_val(d, targetkey):
    if isinstance(d, str):
        for key in targetkey:
            if len(d) - d.find(key) == len(key) and d.find(key) != -1:
                return d.replace(key, targetkey.get(key))
        return d
    elif isinstance(d, list): return [v for v in (map_val(v, targetkey) for v in d)]
    elif isinstance(d, dict): return {k: v for k, v in ((k, map_val(v, targetkey)) for k, v in d.items())}
    else: return d


# Замена $ref
def change_ref(d, targetkey, postfix):
    if not isinstance(d, (dict, list)):
        if 'file:' in str(d): return '#/definitions/' + ((str.split(d, '/')[-1]).split('.')[0]+postfix)
        return d
    elif isinstance(d, list): return [v for v in (change_ref(v, targetkey, postfix) for v in d)]
    else: return {k: v for k, v in ((k, change_ref(v, targetkey,postfix)) for k, v in d.items())}


# объединяем файлы json в модель swagger
def add_json_to_model(dir_schemes_name, f, postfix):
    global model, delNodes, refNodes
    if f.endswith('.json'):
        try:
            with open(dir_schemes_name+"\\"+f, encoding='utf-8') as fh:
                dto = remove_key(json.load(fh), delNodes)
                dto = change_ref(dto, refNodes,postfix)
        except ValueError as e: return False
        model["definitions"][dto["title"]+postfix] = dto
        return True
    return False


# объединяем файлы json в модель swagger (контроллеры + REST запросы)
def add_controllers_to_model(dir_schemes_name, f):
    global model
    if f.endswith('.json'):
        try:
            with open(dir_schemes_name+"\\"+f, encoding='utf-8') as fh:
                controller_json = json.load(fh)
                tags = controller_json['tags']
                paths = controller_json['paths']
        except ValueError as e: return False
        model["tags"] += tags
        model["paths"].update(paths)
        return True
    return False


# добавляем заголовок в результирующий файл JSON модели
with open(file_name_header, encoding='utf-8') as fh:
    model = json.load(fh)

# Обрабатываем схемы модели
json_model_files = [f for f in os.listdir(dir_schemes_name) if add_json_to_model(dir_schemes_name, f, postfix)]

# Обрабатываем схемы рест API
json_schemes_files = [f for f in os.listdir(dir_rest_schemes_name) if add_json_to_model(dir_rest_schemes_name, f, '')]

# Добаваляем контроллер (для примера GET 10 Application)
json_controller_files = [f for f in os.listdir(dir_rest_controllers_name) if add_controllers_to_model(dir_rest_controllers_name,f)]

# Делаем мапинг названий ДТО
# Загружаем JSON с мапингом ключей
with open(dir_dto_map + "\\" + file_name_dto_map_key, encoding='utf-8') as fh:
    dtomap = json.load(fh)

# Заменяем ключи ДТО
model = map_key(model, dtomap)

# Загружаем JSON с мапингом значений (ссылок)
with open(dir_dto_map + "\\" + file_name_dto_map_val, encoding='utf-8') as fh:
    dtomap = json.load(fh)

# Заменяем значение ссылок ДТО
model = map_val(model, dtomap)

# Сохраняем модель SWAGGER в файл
with open(file_name_model, 'w', encoding='utf-8') as outfile:
    json.dump(model, outfile, indent=2, ensure_ascii=False)


