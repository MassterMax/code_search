Запускаем команды из корневой папка, с запущенным и работающим elasticsearch

Для упрощения жизни
```
alias cs='python3 codesearch/cmd/run.py '
```


Создать индекс по схеме
```
cs init index_name
```

Предобработать код
```
make extract_data
```

Добавить данные в индекс
```
cs put index_name
```

Поиск в индексе
```
cs search index_name code

cs search index_name "code searching"
```

Удалить индекс
```
cs delete index_name
```

## masstermax

Установка preprocess - пока что так:
```
pip install git+https://github.com/HSE-JetBrains-department/preprocess@master
```

Для использования в питоне:
```
sudo chmod -R ugo+rX /home/masstermax/.local/lib/python3.8/site-packages/
```

Также для работы нужен go:
```
sudo apt install golang
```

Для запуска run.py:
```
PYTHONPATH=./ python3 codesearch/cmd/run.py %command% %args%
```

### elasticsearch tests
Для работы с тестами я прописал в Makefile команды для запуска эластика, а также подключил 
unittest - это всё для локальных тестов и чтобы поиграть с эластиком, посмотреть, какие
маппинги и запросы можно делать