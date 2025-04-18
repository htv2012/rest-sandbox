import pytest

from rest_sandbox.tools import url_join

ROOT = "http://example.com"
ROOT_SLASH = f"{ROOT}/"


@pytest.mark.parametrize(
    ["paths", "expected"],
    [
        pytest.param([], ROOT, id="no_path"),
        pytest.param(["/"], ROOT, id="root_path"),
        pytest.param(["foo", "bar"], f"{ROOT}/foo/bar", id="multiple_paths"),
        pytest.param(["foo", ""], f"{ROOT}/foo", id="empty_last_component"),
    ],
)
def test_url_join(paths, expected):
    assert url_join(ROOT, *paths) == expected
