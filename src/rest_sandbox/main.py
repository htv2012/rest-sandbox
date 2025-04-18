import cmd
import pathlib
import urllib.parse

import requests
import rich.console

from .tools import url_join


class RestSandbox(cmd.Cmd):
    prompt = "& "
    intro = "Rest Sandbox\n"

    def __init__(self, completekey="tab", stdin=None, stdout=None):
        super().__init__(completekey, stdin, stdout)
        self.pwd = pathlib.Path("/")
        self.home = ""
        self.session = requests.Session()
        self.con = rich.console.Console()

    def do_home(self, home: str):
        parts = urllib.parse.urlsplit(home)
        self.home = urllib.parse.urlunsplit(parts._replace(path=""))

    def do_cd(self, name: str):
        """
        Go to a resource. For example: cd /get
        """
        parts = urllib.parse.urlsplit(name)
        self.pwd /= parts.path
        self.pwd.resolve()

        home = urllib.parse.urlunsplit(parts._replace(path="", query="", fragment=""))
        if home != "":
            self.do_home(home)

    def do_get(self, args: str):
        if args.startswith(("http://", "https://")):
            url = args
        else:
            url = url_join(self.home, self.pwd / args)
        self.con.print(f"GET {url}")
        resp = self.session.get(url)
        self.con.print(f"{resp.status_code} {resp.reason}")
        self.con.print_json(data=resp.json())

    def do_quit(self, _):
        return True

    def emptyline(self):
        pass

    def postcmd(self, stop, line):
        if stop:
            self.session.close()
        else:
            print()
            print(url_join(self.home, self.pwd))

        return stop

    do_EOF = do_quit
    do_q = do_quit
    do_exit = do_quit


def main():
    rest_sandbox = RestSandbox()
    rest_sandbox.cmdloop()
