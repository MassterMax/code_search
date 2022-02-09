# [todo] описание проекта

## Installation

Установка preprocess - пока что так:
```shell
pip install git+https://github.com/HSE-JetBrains-department/preprocess@master
```

Для использования в питоне:
```shell
sudo chmod -R ugo+rX /home/$USER/.local/lib/python3.8/site-packages/
```

Также для работы нужен go:
```shell
sudo apt install golang
```

Для запуска run.py:
```shell
PYTHONPATH=./ python3 codesearch/cmd/run.py %command% %args%
```

## Elasticsearch tests
Для работы с тестами я прописал в Makefile команды для запуска эластика, а также подключил 
unittest - это всё для локальных тестов и чтобы поиграть с эластиком, посмотреть, какие
маппинги и запросы можно делать


## Usage

Запускаем команды из корневой папки, с запущенным и работающим elasticsearch

Можно использовать alias для сокращения комманд
```shell
alias cs='python3 codesearch/cmd/run.py '
```

### Примеры:

Создать индекс по схеме
```shell
cs init index_name
```

Предобработать код
```shell
make extract_data
```

Добавить данные в индекс
```shell
cs put index_name
```

Поиск в индексе
```shell
cs search index_name code

cs search index_name "code searching"
```

Удалить индекс
```shell
cs delete index_name
```