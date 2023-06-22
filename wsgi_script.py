import cgi


def application(environ, start_response):
    ret = list()
    ret.append(b"GET:\n")
    ret.append(str(cgi.urllib.parse.parse_qs(environ["QUERY_STRING"])).encode() + b"\n")
    ret.append(b"POST:\n")
    environ["QUERY_STRING"] = ""
    if environ.get("CONTENT_TYPE") == "application/x-www-form-urlencoded":
        post_param = cgi.parse(fp=environ["wsgi.input"], environ=environ)
        ret.append(str(post_param).encode() + b"\n")
    else:
        ret.append(environ["wsgi.input"].read())
        ret.append(b"\n")

    status = '200 OK'
    response_headers = [('Content-type', 'text/plain')]
    start_response(status, response_headers)
    return ret
