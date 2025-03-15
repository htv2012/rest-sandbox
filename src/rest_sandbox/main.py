import cmd

import requests
import rich.console


class RestSandbox(cmd.Cmd):
    prompt = "& "
    intro = "Rest Sandbox\n"

    def __init__(self, completekey="tab", stdin=None, stdout=None):
        super().__init__(completekey, stdin, stdout)
        self.pwd = ""
        self.session = requests.Session()
        self.con = rich.console.Console()

    def do_get(self, args):
        url = self.pwd + args
        self.con.print(f"GET {url}")
        resp = self.session.get(url)
        self.con.print(f"{resp.status_code} {resp.reason}")
        if not resp.ok:
            pass  # TODO: handle it

        self.con.print_json(data=resp.json())

    def do_cd(self, name):
        """
        Go to a resource. For example: cd https://httpbin.org
        """
        self.pwd = name

    def do_quit(self, _):
        return True

    def emptyline(self):
        pass

    def postcmd(self, stop, line):
        print(f"\n{self.pwd}")

        if stop:
            self.session.close()

        return stop

    do_EOF = do_quit
    do_q = do_quit
    do_exit = do_quit


def main():
    rest_sandbox = RestSandbox()
    rest_sandbox.cmdloop()
