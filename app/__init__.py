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
 5. conform + validate result
 6. format result for output
    + exit non-zero if have error
'''


import json
import os
import requests
import sys
import urllib

from helpers import exit_with_stderr, exit_with_stdout, validate_email, \
                    validate_auth_token, write_to_file, get_auth


url = "http://localhost:5000"

def parse_argv():
    cmd, args = sys.argv[1], sys.argv[2:]
    return cmd, args

def validate_argv(cmd, args):
    # TO DO: incorporate config and env
    if cmd == "signup":
        if len(args) < 1:
            exit_with_stderr("too few command line arguments!")
        elif len(args) > 1:
            exit_with_stderr("too many command line arguments!")
        return args

    elif cmd == "login":
        if len(args) < 1:
            exit_with_stderr("too few command line arguments!")
        elif len(args) > 1:
            exit_with_stderr("too many command line arguments!")
        return args

    elif cmd == "list":
        if len(args) > 0:
            exit_with_stderr("too many command line arguments!")
        return args

    elif cmd == "create":
        if len(args) < 1:
            exit_with_stderr("too few command line arguments!")
        elif len(args) > 1:
            exit_with_stderr("too many command line arguments!")
        return args

    elif cmd == "view":
        if len(args) < 1:
            exit_with_stderr("too few command line arguments!")
        elif len(args) > 1:
            exit_with_stderr("too many command line arguments!")
        return args

    elif cmd == "edit":
        pass
    elif cmd == "access":
        pass
    elif cmd == "upgrade":
        pass
    elif cmd == "disable":
        pass
    else:
        sys.stdout.write("invalid command\n")
        sys.exit(1)

def resolve_argv(cmd, args):
    if cmd == "signup":
        if not validate_email(args[0]):
            exit_with_stderr("invalid e-mail!")

        return {"email": args[0]}

    elif cmd == "login":
        if not validate_auth_token(args[0]):
            exit_with_stderr("invalid auth token!")

        return {"auth_token": args[0]}

    elif cmd == "list":
        auth = get_auth()

        if not auth:
            exit_with_stderr("invalid credentials!")

        return {"auth": auth}

    elif cmd == "create":
        auth = get_auth()

        if not auth:
            exit_with_stderr("invalid credentials!")

        body = {"body": urllib.unquote(args[0])}

        return {"auth": auth, "body": body}

    elif cmd == "view":
        auth = get_auth()

        if not auth:
            exit_with_stderr("invalid credentials!")

        ppgn_token = args[0]

        return {"auth": auth, "ppgn_token": ppgn_token}

    elif cmd == "edit":
        pass
    elif cmd == "access":
        pass
    elif cmd == "upgrade":
        pass
    elif cmd == "disable":
        pass

def request_signup(args):
    result = requests.post(url + "/signup", data=args)
    status_code, result = result.status_code, result.json()

    if status_code == 400:
        exit_with_stdout("email already exists!")

    email = result["user"]["email"]
    auth_token = result["user"]["id"]

    exit_with_stdout("successful signup for {} with id {}".format(email, auth_token))

def request_login(args):
    result = requests.post(url + "/login", data=args)
    status_code, result = result.status_code, result.json()

    if status_code == 400:
        exit_with_stdout("id incorrect!")

    email = result["user"]["email"]
    auth_token = result["user"]["id"]

    data = {
        "EMAIL": email,
        "AUTH_TOKEN": auth_token
    }
    write_to_file(".env", data, "export ")

    exit_with_stdout("successful login for {} with id {}".format(email, auth_token))

def request_list(args):
    result = requests.get(url + "/tost", auth=args["auth"])
    status_code, result = result.status_code, result.json()

    data = {}
    for k, v in result.iteritems():
        data[str(k)] = str(v)

    write_to_file(".temp", data)

    for k, v in data.iteritems():
        sys.stdout.write(k[:4] + ": " + v + "\n")
    sys.exit(0)

def request_create(args):
    result = requests.post(url + "/tost", auth=args["auth"], data=args["body"])
    status_code, result = result.status_code, result.json()

    if status_code == 400:
        exit_with_stdout("body must not be blank!")

    exit_with_stdout("tost created with token {}".format(result["tost"]["access-token"]))

def request_view(args):
    result = requests.get(url + "/tost/" + args["ppgn_token"], auth=args["auth"])
    status_code, result = result.status_code, result.json()

    if status_code == 404:
        exit_with_stdout("tost not found!")

    # TO DO: test redirects
    exit_with_stdout(result["tost"]["body"])

def send_request(cmd, args):
    if cmd == "signup":
        request_signup(args)
    elif cmd == "login":
        request_login(args)
    elif cmd == "list":
        request_list(args)
    elif cmd == "create":
        request_create(args)
    elif cmd == "view":
        request_view(args)
    elif cmd == "edit":
        pass
    elif cmd == "access":
        pass
    elif cmd == "upgrade":
        pass
    elif cmd == "disable":
        pass
