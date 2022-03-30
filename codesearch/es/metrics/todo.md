### Самому размечать данные не понравилось, что можно сделать:
Берём CodeSearchNet - https://github.com/github/CodeSearchNet

Смотрим, как скачать датасет для питона - https://github.com/github/CodeSearchNet/blob/master/notebooks/ExploreData.ipynb

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

Всё это мы получить можем, надо отказаться от location, всё остальное - затычки

Затем, с помощью **hyperopt** оптимизируем коэфы, fuzziness и тд - profit!

Этот же датасет можно заюзать для построения эмбеддингов (+моя домашка по ml4se)