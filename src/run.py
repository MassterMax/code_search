# Запускаем его

import args_parser
import request_rules
from views.init import view as init
from views.search import view as search
from src.views.load_data.load_data import put_to_elastic_search

ERROR_ARGS = "Failed to parser input from: {}"


def main():
    print("Start program")
    while True:
        command = input()
        parser = args_parser.TerminalArgsParser(command)
        if parser.next():
            print(ERROR_ARGS.format(command[:20]))

        # Handle quite command.
        if parser.get_token() in ["q", "quite", "exit"]:
            print("End program")
            return
        method_name = parser.get_token()
        if method_name not in request_rules.ARGS_CONVERTER:
            print("Failed to recognize {}".format(method_name))
            continue

        rules = request_rules.ARGS_CONVERTER[method_name]
        request = {}
        first_error = None
        unnamed_args_ind = 0
        while not parser.next():
            token = parser.get_token()
            if token[0] == '-':
                if token not in rules:
                    first_error = "Failed to recognize {}".format(token)
                    break 
                if not parser.next():
                    parameter_name = rules[token]
                    request[parameter_name] = parser.get_token()
                else:
                    first_error = "Failed to get value after {}".format(token)
                    break
            else:
                if str(unnamed_args_ind) not in rules:
                    first_error = "Too many args {}".format(token)
                    break
                parameter_name = rules[str(unnamed_args_ind)]
                request[parameter_name] = token
                unnamed_args_ind += 1
        if first_error:
            print(first_error)
            continue

        # Костыль, так как я сходу не придумала как вызывать файл по пути views/{method_name}/view.Impl(request, response)
        response = {}
        if method_name == "init":
            init.impl(request, response)
        elif method_name == "search":
            search.impl(request, response)
        elif method_name == 'put':
            response = put_to_elastic_search(request['index_name'])
        if "errors" in response:
            print(response["errors"])


if __name__ == "__main__":
    main()
