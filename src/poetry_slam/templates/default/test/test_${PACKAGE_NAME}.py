import pytest


@pytest.mark.xfail
def test_tests_are_implemented():
    import ${PACKAGE_NAME}
    print("Yyou have not implemented any tests yet.")
    assert False
