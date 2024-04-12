import pytest

from ${PACKAGE_NAME} import cli


@pytest.mark.xfail
def test_tests_are_implemented():
    assert cli.main()
