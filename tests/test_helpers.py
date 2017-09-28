from helpers import validate_email, validate_auth_token
import unittest


class TestCase(unittest.TestCase):

    def test_validate_email(self):
        assert validate_email("alice@example.com") == True
        assert validate_email("alice@example.co.uk") == True
        assert validate_email("alice@example") == False
        assert validate_email("alice") == False

    def test_validate_auth_token(self):
        assert validate_auth_token("abcd1234") == True
        assert validate_auth_token("1234abcd") == True
        assert validate_auth_token("abcdabcd") == True
        assert validate_auth_token("01230123") == True
        assert validate_auth_token("abcdefgh") == False
        assert validate_auth_token("abcdABCD") == False
        assert validate_auth_token("abcd") == False
        assert validate_auth_token("0123") == False
