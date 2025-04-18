import pathlib
import urllib.parse


def url_join(root: str, *paths) -> str:
    path = pathlib.Path("/")
    for dir in paths:
        path /= dir
    path = path.resolve()
    path = str(path)

    parts = urllib.parse.urlsplit(root)
    result = urllib.parse.urlunsplit(parts._replace(path=path))
    result = result.removesuffix("/")
    return result
