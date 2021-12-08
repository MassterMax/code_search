# Из аргументов в терминале может помогать формировать request

ARGS_CONVERTER = {
    "init": {
        "0": "index_name"
    },
    "search": {
        "0": "index_name",
        "1": "search_code_request"
    },
    "put": {
        "0": "index_name"
    },
    'delete': {
        '0': 'index_name'
    },
    'any': {
        '0': 'any_text'
    }
}
