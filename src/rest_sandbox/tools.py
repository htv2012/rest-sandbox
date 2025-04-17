import pathlib
import urllib.parse


def url_join(root: str, path: pathlib.Path) -> str:
    path = path.resolve()
    parts = urllib.parse.urlsplit(root)
    return urllib.parse.urlunsplit(parts._replace(path=str(path)))
