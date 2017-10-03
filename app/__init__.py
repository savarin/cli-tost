import base64
import json
import os
import requests
import sys
import urllib

sys.path.insert(0, "../tost-client")
import tostclient

from helpers import exit_with_stderr, exit_with_stdout, \
                    validate_email, validate_auth_token, \
                    write_to_file


base_domain = "http://localhost:5000"
client = tostclient.TostClient(base_domain)


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
    if cmd == "list":
        return check_args_length(args, 0)

    elif cmd in set(["signup", "login", "create", "view", "access"]):
        return check_args_length(args, 1)

    elif cmd in set(["edit", "upgrade", "disable"]):
        return check_args_length(args, 2)

    exit_with_stderr("invalid command")


def get_headers():
    email = os.getenv("EMAIL")
    auth_token = os.getenv("AUTH_TOKEN")

    return {
        "headers": {
            "Authorization": "Basic " + base64.b64encode(email + ":" + auth_token)
            # "Accept": "bencode"
        }
    }


def add_content(headers, ppgn_token="", data={}):
    headers["ppgn_token"] = ppgn_token
    headers["data"] = data

    return headers


def resolve_argv(cmd, args):
    if cmd == "signup":
        if not validate_email(args[0]):
            exit_with_stderr("invalid e-mail")

        return {"email": args[0]}

    elif cmd == "login":
        if not validate_auth_token(args[0]):
            exit_with_stderr("invalid auth token")

        return {"auth_token": args[0]}

    headers = get_headers()

    if cmd == "list":
        return headers

    elif cmd == "create":
        data = {"body": urllib.unquote(args[0])}
        return add_content(headers, data=data)

    ppgn_token = args[0]

    if cmd in set(["view", "access"]):
        return add_content(headers, ppgn_token=ppgn_token)

    elif cmd == "edit":
        data = {"body": urllib.unquote(args[1])}
        return add_content(headers, ppgn_token=ppgn_token, data=data)

    elif cmd in set(["upgrade", "disable"]):
        data = {"src-access-token": args[1]}
        return add_content(headers, ppgn_token=ppgn_token, data=data)


def compose_request(args, method, cmd):
    try:
        exec("response = client.{}(args, cmd)".format(method))
    except Exception as e:
        exit_with_stderr(str(e))

    if cmd == "login":
        data = {
            "EMAIL": response["data"]["email"],
            "AUTH_TOKEN": response["data"]["auth_token"]
        }
        write_to_file(".env", data)

    elif cmd == "list":
        for k, v in response["data"]["tosts"].iteritems():
            sys.stdout.write(k + ": " + v + "\n")

    elif cmd == "view":
        access_token = response["data"]["tost"]["access-token"]
        body = response["data"]["tost"]["body"]
        exit_with_stdout(access_token + ": " + body)

    elif cmd == "access":
        for k, v in response["data"]["propagations"].iteritems():
            sys.stdout.write(v["access-token"] + ": " + k + "\n")

    exit_with_stdout(response["msg"])


def send_request(cmd, args):
    if cmd in set(["signup", "login"]):
        compose_request(args, "start", cmd)

    elif cmd == "list":
        compose_request(args, "multiple", cmd)

    elif cmd in set(["create", "view", "edit"]):
        compose_request(args, "individual", cmd)

    elif cmd == "access":
        compose_request(args, "permit", cmd)

    elif cmd in set(["upgrade", "disable"]):
        compose_request(args, "switch", cmd)
