import pytest

from rest_sandbox.tools import url_join

ROOT = "http://example.com"


@pytest.mark.parametrize(
    ["root", "path", "expected"],
    [
        pytest.param(ROOT, "", ROOT, id="without_end_slash"),
        pytest.param(ROOT, "/", ROOT, id="with_end_slash"),
        pytest.param(ROOT, "foo/bar", f"{ROOT}/foo/bar", id="multiple_paths"),
    ],
)
def test_url_join(root, path, expected):
    assert url_join(root, path) == expected
