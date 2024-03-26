import subprocess
from dataclasses import dataclass
from unittest.mock import MagicMock

import pytest

from poetry_slam.build_tool import BuildError, BuildTool


def result_factory(out: bytes = b"", err: bytes = b"", code: int = 0):
    @dataclass
    class returnval:
        stdout: bytes = out
        stderr: bytes = err
        returncode: int = code

    return MagicMock(spec=subprocess, **{"run.return_value": returnval()})


@pytest.mark.parametrize(
    "out, err, returncode, exception_type",
    [
        (b"", b"", 0, None),
        (b"", b"some error", 1, BuildError),
    ],
)
def test_slam(monkeypatch, out, err, returncode, exception_type):
    monkeypatch.setattr("poetry_slam.build_tool.subprocess", result_factory(out, err, returncode))
    try:
        assert BuildTool().build() == returncode
    except exception_type:
        pass


def test_format(monkeypatch):
    monkeypatch.setattr("poetry_slam.build_tool.subprocess", result_factory())
    assert BuildTool().auto_format() == 0


def test_install(monkeypatch):
    monkeypatch.setattr("poetry_slam.build_tool.subprocess", result_factory())
    assert BuildTool().install() == 0


def test_test(monkeypatch):
    monkeypatch.setattr("poetry_slam.build_tool.subprocess", result_factory(out=b"out", err=b"err", code=0))
    assert BuildTool(verbose=True).test([]) == 0
