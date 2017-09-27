from app import parse_argv, validate_argv, resolve_argv, send_request
    

if __name__ == "__main__":
    cmd, args = parse_argv()
    args = validate_argv(cmd, args)
    args = resolve_argv(cmd, args)

    send_request(cmd, args)
