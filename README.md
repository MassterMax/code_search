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