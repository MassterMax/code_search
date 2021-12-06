def check_request(method, request):
    return True


def make_error(response, error):
    if "errors" not in response:
        response["errors"] = error
    else:
        response["errors"].append(error)


def try_open_file(path):
    try:
        return open(path, "r")
    except IOError:
        return None
