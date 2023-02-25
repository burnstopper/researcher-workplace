# Инструкция по использованию скрипта

## Окружение
Для работы требуется python3.

Список зависимостей:
1. openpyxl - 3.0+
2. pandas - 1.5+

Установить все зависимости можно командой
```
pip install -r requirements/win-dev.txt
```

## Загрузка данных из xlsx файла
При загрузке результатов из xlsx файла в качестве идентификатора пользователя используется имя файла без расширения.
Если файл, из которого заргужаются резльутаты называется `gdrive_results/Респондент_010.xlsx`, то идентификатор
респондента `Респондент_010`.

### Индивидуальная загрузка результатов из файла
Загрузить результаты 10 респондента из файла `./gdrive_results/Респондент_010.xlsx` и сохранить в БД sqlite `out/results.sqlite`
```
python -m app --xls -f gdrive_results/Респондент_010.xlsx -o out -k xls-file-loader
```

### Пакетная загрузка результатов из папки
Загрузить результаты всех респондентов из папки `gdrive_results` и сохранить в БД sqlite `out/results.sqlite`.
```
python -m app --xls -d gdrive_results -o out -k xls-folder-loader
```

## Загрузка результатов из таблицы с результатами из google form
Загрузить результаты респондентов, проешедших опрос в google forms и сохранить их в БД sqlite `out/results.sqlite`
```
python -m app --gform -f gform_results/response.xlsx -o out -k gform-file-loader
```

## Указание источника данных
При загрузке данных можно указать ключ источника данных. Для этого используется опциональный параметр командной строки `-k`.
```
python -m app --xls -d hse_webinar_24_11_22 -o out -k "hse-webinar-24-11-22"
```
Данный вызов загрузит результаты всех участников в БД из папки `hse_webinar_24_11_22` и пометит все добавленные строки ключом `hse-webinar-24-11-22`.
