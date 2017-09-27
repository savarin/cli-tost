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

