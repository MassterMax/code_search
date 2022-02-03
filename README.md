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


### notes - full work
```
PYTHONPATH=./ python3 codesearch/cmd/run.py extract /mnt/c/Users/maxma/Documents/GitHub/code_search/codesearch/preproc/repositories.csv /mnt/c/Users/maxma/Documents/ /mnt/c/Users/maxma/Documents/GitHub/code_search/codesearch/preproc/ 8

PYTHONPATH=./ python3 codesearch/cmd/run.py init code_index_2

PYTHONPATH=./ python3 codesearch/cmd/run.py put code_index_2 /mnt/c/Users/maxma/Documents/GitHub/code_search/codesearch/preproc/

PYTHONPATH=./ python3 codesearch/cmd/run.py search2 code_index_2 /mnt/c/Users/maxma/Documents/GitHub/code_search/codesearch/es/example_request.json

PYTHONPATH=./ python3 codesearch/cmd/run.py delete code_index_2
```