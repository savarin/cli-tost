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

from helpers import exit_with_stderr, exit_with_stdout, validate_email, \
                    validate_auth_token, write_to_env


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
        pass
    elif cmd == "create":
        pass
    elif cmd == "view":
        pass
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
        pass
    elif cmd == "create":
        pass
    elif cmd == "view":
        pass
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
        exit_with_stdout(result["msg"])

    email = result["user"]["email"]
    auth_token = result["user"]["id"]

    exit_with_stdout("successful signup for {} with id {}".format(email, auth_token))

def request_login(args):
    result = requests.post(url + "/login", data=args)
    status_code, result = result.status_code, result.json()

    if status_code == 400:
        exit_with_stdout(result["msg"])

    email = result["user"]["email"]
    auth_token = result["user"]["id"]
    data = {
        "EMAIL": result["user"]["email"],
        "AUTH_TOKEN": result["user"]["id"]
    }

    write_to_env(".env", data)
    exit_with_stdout("successful login for {} with id {}".format(email, auth_token))

def send_request(cmd, args):
    if cmd == "signup":
        request_signup(args)
    elif cmd == "login":
        request_login(args)
    elif cmd == "list":
        pass
    elif cmd == "create":
        pass
    elif cmd == "view":
        pass
    elif cmd == "edit":
        pass
    elif cmd == "access":
        pass
    elif cmd == "upgrade":
        pass
    elif cmd == "disable":
        pass