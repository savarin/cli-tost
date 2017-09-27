from helpers import validate_email
import unittest


class TestCase(unittest.TestCase):

    def test_validate_email(self):
        assert validate_email("alice@example.com") == True
        assert validate_email("alice@example.co.uk") == True
        assert validate_email("alice@example") == False
        assert validate_email("alice") == False
