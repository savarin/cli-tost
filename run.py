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