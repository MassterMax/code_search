## Introduction
**Codesearch** - это проект, который позволяет искать нужный код среди популярных гитхаб-репозиториев
с запросами на natural language с возможностью фильтрации, ранжирования и паджинации данных.

## Baseline
В качестве бейзлайна используется **elasticsearch** и **10000** наиболее популярных репозиториев на языке
**Python**. Данные извлекаются из репозиториев, складываются в индекс elasticsearch, а затем,
с помощью раличных маппингов и конструктора запросов, можно искать код.

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

```shell
alias cs='python3 codesearch/cmd/run.py '
```

Для установки зависимостей и создания модуля нужно запустить из корневой папки команду
```shell
pip install -e .
```

## Elasticsearch tests
Для работы с тестами я прописал в Makefile команды для запуска эластика, а также подключил 
unittest - это всё для локальных тестов и чтобы поиграть с эластиком, посмотреть, какие
маппинги и запросы можно делать


## Usage

Запускаем команды из корневой папки, с запущенным и работающим elasticsearch

### Примеры:

Создать индекс по схеме
```shell
cs init index_name
```

Предобработать код
```shell
cs extract git/repositories/urls.csv working/directory/for/temporaty/files/ directory/where/to/write/result/
```

Добавить  в индекс данные, сложенные в папку results на предыдущем шаге
```shell
cs put index_name results
```

Поиск в индексе
```shell
cs search index_name code

cs search index_name "code searching"
```

Поиск в индексе, запрос записан в виде json
```shell
cs search2 index_name path/to/request.json
```


Удалить индекс
```shell
cs delete index_name
```