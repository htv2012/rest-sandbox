import cmd
import pathlib
import urllib.parse

import requests
import rich.console


def url_join(root: str, path: pathlib.Path) -> str:
    path = path.resolve()
    parts = urllib.parse.urlsplit(root)
    return urllib.parse.urlunsplit(parts._replace(path=str(path)))


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
        self.pwd = (self.pwd / name).resolve()

    def do_get(self, args: str):
        #        args = args.strip().removeprefix("/")
        #        if self.pwd:
        #            url = f"{self.pwd}/{args}"
        #        else:
        #            url = args
        # url = url.removeprefix("/").removesuffix("/")
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
            print(url_join(self.home, self.pwd))

        return stop

    do_EOF = do_quit
    do_q = do_quit
    do_exit = do_quit


def main():
    rest_sandbox = RestSandbox()
    rest_sandbox.cmdloop()
