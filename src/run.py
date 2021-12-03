# Запускаем его

import args_parser
import request_rules
from views.init import view as init

ERROR_ARGS = "Failed to parser input from: {}"

def main():
    print("Start programe")
    while True:
        command = input()
        parser = args_parser.TerminalArgsParser(command)
        if parser.next():
            print(ERROR_ARGS.format(command[:20]))

        # Handle quite command.
        if parser.get_tocken() in ["q", "quite", "exit"]:
            print("End programe")
            return
        method_name = parser.get_tocken()
        if method_name not in request_rules.ARGS_CONVERTER:
            print("Failed to recognize {}".format(method_name))
            continue
        
        rules = request_rules.ARGS_CONVERTER[method_name]
        request = {}
        first_error = None
        unnamed_args_ind = 0
        while not parser.next():
            tocken = parser.get_tocken()
            if tocken[0] == '-':
                if tocken not in rules:
                    first_error = "Failed to recognize {}".format(tocken)
                    break 
                if not parser.next():
                    parameter_name = rules[tocken]
                    request[parameter_name] = parser.get_tocken()
                else:
                    first_error = "Failed to get value after {}".format(tocken)
                    break
            else:
                if str(unnamed_args_ind) not in rules:
                    first_error = "Too many args {}".format(tocken)
                    break
                parameter_name = rules[str(unnamed_args_ind)]
                request[parameter_name] = tocken
        if first_error:
            print(first_error)
            continue
        response = {}
        # Костыль, так как я сходу не придумала как вызывать файл по пути views/{method_name}/view.Impl(request, response)
        if method_name == "init":
            init.Impl(request, response)
            if "errors" in response:
                print(response["errors"])
            else:
                print(response["template"].format(response["index_name"]))


if __name__ == "__main__":
    main()