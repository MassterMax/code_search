def check_request(method, request):
    return True

def make_error(respone, error):
    if "errors" not in respone:
        respone["errors"] = (error)
    else:
        respone["errors"].append(error)

def try_open_file(path):
    try:
        return open(path, "r")
    except IOError:
        return None