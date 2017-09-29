import commands
import requests
import sys
import unittest


class TestCase(unittest.TestCase):

    def setUp(self):
        self.email_0 = "alice@example.com"
        self.email_1 = "bob@example.com"
        self.email_2 = "carol@example.com"
        self.email_3 = "david@example.com"
        self.auth_token_0 = ""
        self.auth_token_1 = ""
        self.auth_token_2 = ""
        self.auth_token_3 = ""

    def sign_up(self, email):
        cmd = "./job.sh signup " + email
        exit_code, msg = commands.getstatusoutput(cmd)
        auth_token = msg.split(" ")[-1]

        cmd = "./job.sh login " + auth_token
        exit_code, msg = commands.getstatusoutput(cmd)

        return auth_token

    def test_signup(self):
        cmd = "./job.sh signup " + self.email_0
        exit_code, msg = commands.getstatusoutput(cmd)
        self.assertEqual(exit_code, 0)
        self.assertIn("alice@example.com", msg)

        exit_code, msg = commands.getstatusoutput(cmd)
        self.assertEqual(exit_code >> 8, 1)
        self.assertIn("already signed up with that email", msg)

    def test_login(self):
        cmd = "./job.sh signup " + self.email_0
        exit_code, msg = commands.getstatusoutput(cmd)
        self.auth_token_0 = msg.split(" ")[-1]

        cmd = "./job.sh login " + self.auth_token_0
        exit_code, msg = commands.getstatusoutput(cmd)
        self.assertEqual(exit_code, 0)
        self.assertIn("alice@example.com", msg)

        cmd = "./job.sh login " + "abcd0123"
        exit_code, msg = commands.getstatusoutput(cmd)
        self.assertEqual(exit_code >> 8, 1)
        self.assertIn("invalid token", msg)

    def test_index(self):
        self.auth_token_0 = self.sign_up(self.email_0)

        cmd = "./job.sh create " + "foo"
        exit_code, msg = commands.getstatusoutput(cmd)

        cmd = "./job.sh index"
        exit_code, msg = commands.getstatusoutput(cmd)
        self.assertEqual(exit_code, 0)
        self.assertIn("foo", msg)

    def test_create(self):
        self.auth_token_0 = self.sign_up(self.email_0)

        cmd = "./job.sh create " + "foo"
        exit_code, msg = commands.getstatusoutput(cmd)
        print msg
        self.assertEqual(exit_code, 0)
        self.assertIn("successful create for tost with access-token", msg)

        cmd = "./job.sh create " + ""
        exit_code, msg = commands.getstatusoutput(cmd)
        self.assertEqual(exit_code >> 8, 1)
        self.assertIn("too few command line arguments!", msg)

    def test_view(self):
        self.auth_token_0 = self.sign_up(self.email_0)

        cmd = "./job.sh create " + "foo"
        exit_code, msg = commands.getstatusoutput(cmd)
        ppgn_token_0 = msg.split(" ")[-1]

        # case 3: user is creator of tost that propagation points to
        cmd = "./job.sh view " + msg.split(" ")[-1]
        exit_code, msg = commands.getstatusoutput(cmd)
        print msg
        self.assertEqual(exit_code, 0)
        self.assertIn("foo", msg)

        # case 2: user visits resource for the first time
        self.auth_token_1 = self.sign_up(self.email_1)

        cmd = "./job.sh view " + ppgn_token_0
        exit_code, msg = commands.getstatusoutput(cmd)
        ppgn_token_1 = msg.split(": ")[0]

        cmd = "./job.sh view " + ppgn_token_1
        exit_code, msg = commands.getstatusoutput(cmd)
        self.assertEqual(exit_code, 0)
        self.assertIn("foo", msg)

        # case 4: user propagation is of lower priority than propagation in url
        self.auth_token_2 = self.sign_up(self.email_2)

        cmd = "./job.sh view " + ppgn_token_1
        exit_code, msg = commands.getstatusoutput(cmd)

        cmd = "./job.sh view " + ppgn_token_0
        exit_code, msg = commands.getstatusoutput(cmd)
        ppgn_token_2 = msg.split(": ")[0]

        cmd = "./job.sh view " + ppgn_token_2
        exit_code, msg = commands.getstatusoutput(cmd)
        self.assertEqual(exit_code, 0)
        self.assertIn("foo", msg)

        # case 5: user propagation is of higher priority than propagation in url
        self.auth_token_3 = self.sign_up(self.email_3)

        cmd = "./job.sh view " + ppgn_token_0
        exit_code, msg = commands.getstatusoutput(cmd)

        cmd = "./job.sh view " + ppgn_token_1
        exit_code, msg = commands.getstatusoutput(cmd)
        ppgn_token_3 = msg.split(": ")[0]

        cmd = "./job.sh view " + ppgn_token_3
        exit_code, msg = commands.getstatusoutput(cmd)
        self.assertEqual(exit_code, 0)
        self.assertIn("foo", msg)

        # case 1: propagation invalid
        cmd = "./job.sh login " + self.auth_token_1
        exit_code, msg = commands.getstatusoutput(cmd)

        cmd = "./job.sh view " + "foo"
        exit_code, msg = commands.getstatusoutput(cmd)
        self.assertEqual(exit_code >> 8, 1)
        self.assertIn("tost not found", msg)

    def test_edit(self):
        self.auth_token_0 = self.sign_up(self.email_0)

        cmd = "./job.sh create " + "foo"
        exit_code, msg = commands.getstatusoutput(cmd)

        cmd = "./job.sh edit " + msg.split(" ")[-1] + " " + "bar"
        exit_code, msg = commands.getstatusoutput(cmd)
        self.assertEqual(exit_code, 0)
        self.assertIn("successful edit for tost with access-token", msg)

    # def test_access(self):
    #     self.auth_token_0 = self.sign_up(self.email_0)

    #     cmd = "./job.sh create " + "foo"
    #     exit_code, msg = commands.getstatusoutput(cmd)
    #     ppgn_token_0 = msg.split(" ")[-1]

    #     self.auth_token_1 = self.sign_up(self.email_1)

    #     cmd = "./job.sh view " + ppgn_token_0
    #     exit_code, msg = commands.getstatusoutput(cmd)

    #     cmd = "./job.sh login " + self.auth_token_0
    #     exit_code, msg = commands.getstatusoutput(cmd)

    #     cmd = "./job.sh access " + ppgn_token_0
    #     exit_code, msg = commands.getstatusoutput(cmd)
    #     self.assertEqual(exit_code, 0)
    #     self.assertIn(self.email_1, msg)

    # def test_upgrade(self):
    #     self.auth_token_0 = self.sign_up(self.email_0)

    #     cmd = "./job.sh create " + "foo"
    #     exit_code, msg = commands.getstatusoutput(cmd)
    #     ppgn_token_0 = msg.split(" ")[-1]

    #     self.auth_token_1 = self.sign_up(self.email_1)

    #     cmd = "./job.sh view " + ppgn_token_0
    #     exit_code, msg = commands.getstatusoutput(cmd)
    #     ppgn_token_1 = msg.split(": ")[0]

    #     self.auth_token_2 = self.sign_up(self.email_2)

    #     cmd = "./job.sh view " + ppgn_token_1
    #     exit_code, msg = commands.getstatusoutput(cmd)
    #     ppgn_token_2 = msg.split(": ")[0]

    #     cmd = "./job.sh login " + self.auth_token_0
    #     exit_code, msg = commands.getstatusoutput(cmd)

    #     cmd = "./job.sh upgrade " + ppgn_token_0 + " " + ppgn_token_2
    #     exit_code, msg = commands.getstatusoutput(cmd)
    #     self.assertEqual(exit_code, 0)
    #     self.assertIn("successful access token upgrade", msg)

    #     cmd = "./job.sh login " + self.auth_token_1
    #     exit_code, msg = commands.getstatusoutput(cmd)

    #     cmd = "./job.sh upgrade " + ppgn_token_1 + " " + ppgn_token_2
    #     exit_code, msg = commands.getstatusoutput(cmd)
    #     self.assertEqual(exit_code >> 8, 1)
    #     self.assertIn("access token is not ancestor to source!", msg)

    # def test_disable(self):
    #     self.auth_token_0 = self.sign_up(self.email_0)

    #     cmd = "./job.sh create " + "foo"
    #     exit_code, msg = commands.getstatusoutput(cmd)
    #     ppgn_token_0 = msg.split(" ")[-1]

    #     self.auth_token_1 = self.sign_up(self.email_1)

    #     cmd = "./job.sh view " + ppgn_token_0
    #     exit_code, msg = commands.getstatusoutput(cmd)
    #     ppgn_token_1 = msg.split(": ")[0]

    #     cmd = "./job.sh login " + self.auth_token_0
    #     exit_code, msg = commands.getstatusoutput(cmd)

    #     cmd = "./job.sh disable " + ppgn_token_0 + " " + ppgn_token_1
    #     exit_code, msg = commands.getstatusoutput(cmd)
    #     self.assertEqual(exit_code, 0)
    #     self.assertIn("successful access token disable", msg)

    #     cmd = "./job.sh disable " + ppgn_token_0 + " " + ppgn_token_1
    #     exit_code, msg = commands.getstatusoutput(cmd)
    #     self.assertEqual(exit_code >> 8, 1)
    #     self.assertIn("source is not descendant to access token!", msg)

    def tearDown(self):
        requests.get("http://127.0.0.1:5000/reset")
