# Инструкция по использованию скрипта

## Окружение
Для работы требуется python3 и библиотека openpyxl.

Рекоммендуется использовать PowerShell и виртуальное окружение `venv`.
```
python -m venv venv
venv\Scripts\Activate.ps1
```

Установить зависимости командой
```
pip install -r requirements/win-dev.txt
```

## Использование
Загрузить результаты 10 респондента из файла `./gdrive_results/Респондент_010.xlsx` и сохранить в БД sqlite `out/results.sqlite`
```
python -m app 10 -s gdrive_results -d out
```
