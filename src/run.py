import json
from pprint import pprint
from shutil import Error

from elasticsearch import Elasticsearch
import elasticsearch

import args_parser
import request_rules
from views.init import view as init
from views.search import view as search
from views.load_data.load_data import put_to_elastic_search, delete
ERROR_ARGS = "Failed to parser input from: {}"


def main():
    es = None
    try:
        es = Elasticsearch()
    except (elasticsearch.exceptions.ConnectionError, elasticsearch.exceptions.ConnectionTimeout) as error:
        print("Failed to connect es:", error)
        return
    last_method = None
    last_index = None
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
        request = {}
        unnamed_args_ind = 0
        if parser.get_token() in [None, "r"]:
            if last_method is None:
                print("Failed to get previous command")
                continue
            method_name = last_method
            request["index_name"] = last_index
            unnamed_args_ind += 1
        else:
            method_name = parser.get_token()
            if method_name not in request_rules.ARGS_CONVERTER:
                print("Failed to recognize {}".format(method_name))
                continue

        rules = request_rules.ARGS_CONVERTER[method_name]
        first_error = None
        while not parser.next() and not parser.is_end():            
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

        try:
            response = {}
            if method_name == 'put':
                response = put_to_elastic_search(request['index_name'], es)
            elif method_name == 'delete':
                response = delete(request['index_name'], es)
            elif method_name == 'any':
                text = request['any_text']
                response = es.search(body=json.load(text))
            else:
                eval(method_name + ".impl(request, response, es)")
            pprint(response)
            last_method = method_name
            last_index = request["index_name"]
        except Exception as e:
           print(f'ooops!: {e}')


if __name__ == "__main__":
    main()
