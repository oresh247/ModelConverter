Create swagger model from json schemes 
=============================

Требования к развертыванию
--------------------------
Для работы скрипта необходимо разместить данные в требуемой структуре:

- \definitions # каталог обработки файлов схем модели
- \paths\schemes # каталог обработки файлов схем рест запросов
- \paths' # каталог обработки файлов схем рест контроллеров
- header.json # требуемый заголовок и пустая структура в схеме swagger 

Задать глобальные переменные в скрипте main.py

- delNodes = ['$schema', '$comment','dependencies'] # удаляемые блоки
- refNodes = ['$ref'] # блоки, где меняем ссылки
- dir_root =r'C:\_GITLAB\modelconverter' # корневой каталог
- dir_schemes_name = dir_root + r'\definitions' # каталог обработки файлов схем модели
- dir_rest_schemes_name = dir_root + r'\paths\schemes' # каталог обработки файлов схем рест запросов
- dir_rest_controllers_name = dir_root + r'\paths' # каталог обработки файлов схем рест контроллеров
- dir_dto_map = dir_root + r'\map' # Каталог расположения файлов мапинга
- file_name_header = 'header.json' # Файл с заголовком для модели SWAGGER
- file_name_model = 'model.json' # Генерируемый файл итоговой модели
- file_name_dto_map_key = 'dtomapkey.json' # Замена самих названий ДТО
- file_name_dto_map_val = 'dtomapval.json' # Замена названий в ссылках на ДТО (иногда надо заменить только ссылки без замены названия ДТО)
- postfix = 'Dto' # Добавляется к названию схемы (так сейчас сделано в разработке)

Результат
---------
Результатом выполнения скрипта будет файл model.json, который может интерпретироваться с помощью swagger

- https://editor.swagger.io/ (Файл->Импорт файл)