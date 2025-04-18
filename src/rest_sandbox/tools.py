import os
import urllib.parse


def url_join(root: str, path) -> str:
    path = os.path.normpath(path or "/")
    parts = urllib.parse.urlsplit(root)
    result = urllib.parse.urlunsplit(parts._replace(path=path))
    result = result.rstrip("/")
    return result
