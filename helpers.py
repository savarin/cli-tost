import os
import re
import requests
import sys


def exit_with_stdout(comments):
    sys.stderr.write(comments + "\n")
    sys.exit(0)

def exit_with_stderr(comments):
    sys.stderr.write(comments + "\n")
    sys.exit(1)

def validate_email(email):
    if not (len(email.split("@")) == 2 and
            len(email.split("@")[-1].split(".")) >= 2):
        return False
    return True

def validate_auth_token(auth_token):
    if not (len(auth_token) == 8 and
            re.match("^[a-f0-9]*$", auth_token)):
        return False
    return True

def write_to_file(path, data, prefix=""):
    with open(path, "w") as f:
        for k, v in data.iteritems():
            f.write(prefix + '{}="{}"\n'.format(k, v))

def get_auth():
    email = os.getenv("EMAIL")
    auth_token = os.getenv("AUTH_TOKEN")

    if not (validate_email(email) and 
            validate_auth_token(auth_token)):
        return False

    return requests.auth.HTTPBasicAuth(email, auth_token)
