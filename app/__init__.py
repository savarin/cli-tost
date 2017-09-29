'''
commands = signup, login, list, create, view, edit, access, upgrade, disable

 1. confirm argv + other input to data structure in deterministic way
    - read in order i. config ii. env iii. argv, later overrides earlier
    - e.g. {"cmd": ["access", "move"],
            "args": ["7b31", ...]}
 2. validate input, conform specifically
    - e.g. {"cmd": "access_move",
            "post_token": "7b31",
            "from_email": "bob@...""}
 3. resolve to "real" values
    - i.e. from abbreviation into full token
    - e.g. {"cmd": "access_move",
            "from_token": "abc123..."
 4. make network call
 5. conform + validate response
 6. format response for output
    + exit non-zero if have error
'''


import json
import os
import requests
import sys
import urllib


sys.path.insert(0, "../tost-client")
import tostclient


from helpers import exit_with_stderr, exit_with_stdout, validate_email, \
                    validate_auth_token, write_to_file


base_domain = "http://localhost:5000"
request = tostclient.TostClient(base_domain)


def parse_argv():
    cmd, args = sys.argv[1], sys.argv[2:]
    return cmd, args


def check_args_length(args, length):
    if len(args) < length:
        exit_with_stderr("too few command line arguments!")
    if len(args) > length:
        exit_with_stderr("too many command line arguments!")
    return args


def validate_argv(cmd, args):
    # TO DO: incorporate config and env
    if cmd == "index":
        return check_args_length(args, 0)

    elif cmd in set(["signup", "login", "create", "view", "access"]):
        return check_args_length(args, 1)

    elif cmd in set(["edit", "upgrade", "disable"]):
        return check_args_length(args, 2)

    sys.stdout.write("invalid command\n")
    sys.exit(1)


def get_auth():
    email = os.getenv("EMAIL")
    auth_token = os.getenv("AUTH_TOKEN")

    if not (validate_email(email) and
            validate_auth_token(auth_token)):
        exit_with_stderr("invalid credentials!")

    return {"auth": requests.auth.HTTPBasicAuth(email, auth_token)}


def add_content(auth, ppgn_token="", data={}):
    auth["ppgn_token"] = ppgn_token
    auth["data"] = data

    return auth


def resolve_argv(cmd, args):
    if cmd == "signup":
        if not validate_email(args[0]):
            exit_with_stderr("invalid e-mail!")

        return {"email": args[0]}

    elif cmd == "login":
        if not validate_auth_token(args[0]):
            exit_with_stderr("invalid auth token!")

        return {"auth_token": args[0]}

    elif cmd == "index":
        return get_auth()

    elif cmd == "create":
        auth = get_auth()
        data = {"body": urllib.unquote(args[0])}

        return add_content(auth, data=data)

    elif cmd in set(["view", "access"]):
        auth = get_auth()
        ppgn_token = args[0]

        return add_content(auth, ppgn_token=ppgn_token)

    elif cmd == "edit":
        auth = get_auth()
        ppgn_token = args[0]
        data = {"body": urllib.unquote(args[1])}

        return add_content(auth, ppgn_token=ppgn_token, data=data)

    elif cmd in set(["upgrade", "disable"]):
        auth = get_auth()
        ppgn_token = args[0]
        data = {"src-access-token": args[1]}

        return add_content(auth, ppgn_token=ppgn_token, data=data)


def request_signup(args):
    try:
        response = request.start(args, "signup")
    except Exception as e:
        exit_with_stderr(str(e))

    exit_with_stdout(response["msg"])


def request_login(args):
    try:
        response = request.start(args, "login")
    except Exception as e:
        exit_with_stderr(str(e))

    data = {
        "EMAIL": response["data"]["email"],
        "AUTH_TOKEN": response["data"]["auth_token"]
    }
    write_to_file(".env", data)

    exit_with_stdout(response["msg"])


def request_index(args):
    try:
        response = request.index(args, "tost")
    except Exception as e:
        exit_with_stderr(str(e))

    for k, v in response["data"]["tosts"].iteritems():
        sys.stdout.write(k[:4] + ": " + v + "\n")
    sys.exit(0)


def request_create(args):
    try:
        response = request.create(args, "tost")
    except Exception as e:
        exit_with_stderr(str(e))

    exit_with_stdout(response["msg"])


def request_view(args):
    try:
        response = request.view(args, "tost")
    except Exception as e:
        exit_with_stderr(str(e))

    access_token = response["data"]["tost"]["access-token"]
    body = response["data"]["tost"]["body"]

    exit_with_stdout(access_token + ": " + body)


def request_edit(args):
    try:
        response = request.edit(args, "tost")
    except Exception as e:
        exit_with_stderr(str(e))

    exit_with_stdout(response["msg"])


    # domain = base_domain + "/tost/" + args["ppgn_token"]
    # response = requests.put(domain, auth=args["auth"], data=args["data"])
    # status_code, response = response.status_code, response.json()

    # if status_code == 404:
    #     exit_with_stderr("tost not found!")

    # if status_code == 302:
    #     exit_with_stderr("please use refreshed access token {}"
    #                      .format(response["access-token"]))

    # exit_with_stdout("successful tost edit")


def request_access(args):
    domain = base_domain + "/tost/" + args["ppgn_token"] + "/propagation"
    response = requests.get(domain, auth=args["auth"])
    status_code, response = response.status_code, response.json()

    for k, v in response["propagations"].iteritems():
        sys.stdout.write(str(k) + ": " + str(v["access-token"]) + "\n")
    sys.exit(0)


def request_upgrade(args):
    domain = base_domain + "/tost/" + args["ppgn_token"] + "/propagation/upgrade"
    response = requests.post(domain, auth=args["auth"], data=args["data"])
    status_code, response = response.status_code, response.json()

    if status_code == 400:
        exit_with_stderr("access token is not ancestor to source!")

    exit_with_stdout("successful access token upgrade")


def request_disable(args):
    domain = base_domain + "/tost/" + args["ppgn_token"] + "/propagation/disable"
    response = requests.post(domain, auth=args["auth"], data=args["data"])
    status_code, response = response.status_code, response.json()

    if status_code == 400:
        exit_with_stderr("source is not descendant to access token!")

    exit_with_stdout("successful access token disable")


def send_request(cmd, args):
    if cmd == "signup":
        request_signup(args)

    elif cmd == "login":
        request_login(args)

    elif cmd == "index":
        request_index(args)

    elif cmd == "create":
        request_create(args)

    elif cmd == "view":
        request_view(args)

    elif cmd == "edit":
        request_edit(args)

    elif cmd == "access":
        request_access(args)

    elif cmd == "upgrade":
        request_upgrade(args)

    elif cmd == "disable":
        request_disable(args)
