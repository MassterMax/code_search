### Самому размечать данные не понравилось, что можно сделать:
Берём CodeSearchNet - https://github.com/github/CodeSearchNet

note для **masstermax** - фулл распакованный датасет без всяких .pkl весит ~ 1.7 ГБ

Смотрим, как скачать датасет для питона:
```shell
https://github.com/github/CodeSearchNet/blob/master/notebooks/ExploreData.ipynb
```

```shell
!wget https://s3.amazonaws.com/code-search-net/CodeSearchNet/v2/python.zip
```


В данных уже есть тело функции, identifiers функции, комментарий 
Также можно выделить имя функции исходя из identifiers + сделать сплит через **preprocess.mappers.utils.TokenParser**

Вообще в запросе мы хотим проставить коэффициенты:

```python
fields = [
    # exact occurrence
    "identifiers^2",
    "split_identifiers^2",
    "function_body^2",
    # meaning
    "docstring^4",
    "location"
    "function_name^2",
]
```

Всё это мы получить можем, мб отказаться от location, всё остальное - затычки

Затем, с помощью **hyperopt** оптимизируем коэфы, fuzziness и тд - profit!

Этот же датасет можно заюзать для построения эмбеддингов (+моя домашка по ml4se)


## todo - было бы неплохо понять, что мы хотим оптимизировать?
- коэффициенты после полей
- fuzziness 
- методы поиска (multi query и тд)
- потом - поиск по эмбеддингам?
- ВОЗМОЖНО СТОИТ ЗАМЕНИТЬ АНАЛИЗАТОРЫ НА N-ГРАММЫ!!!

## какие метрики?
- MAP - среднее по average precision - у нас это было среднее по 1/n, где n - позиция в выдаче
- top-N - 1 - если есть в N верхних, 0 иначе, всё усредняем