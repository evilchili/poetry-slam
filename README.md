# poetry-slam

An opinionated build tool for python poetry projects, poetry-slam saves me having to add boilerplate build scripts to every project for things like tests, coverage, package installation, automatic formatting, and so on.

## Installation

Clone the repository and install slam locally:

```bash
% git clone https://github.com/evilchili/poetry-slam.git
% cd poetry-slam
% poetry build
% pip3 install dist/*.whl
```

## Basic Usage:

Use `slam` to build your projects. Your package source must be in the `src/` directory, and your tests must be in `test/`. The most common usage, and the default, if no command is specified, is to do a `build`,
which formats your source, tests it, (re)installs the source packages to your virtual environment, and does a release build all in one step:

```bash
% cd /some/poetry-project/
% slam build
Formatting...
Testing...
Installing...
Building...
slam build: SUCCESS
```

You can also run individual steps; see `slam --help` for details.

### Testing With Pytest

Anything passed to `slam test` will be passed directly to pytest as command-line arguments. So for example:

```bash
% slam test -vv -k test_this_one_thing
```


### Debugging

Get gory details with the combination of `--verbose` and `--log-level` most suitable to your liking:

```bash
% slam --verbose --log-level=DEBUG build

Formatting...
[03/25/24 22:21:32] INFO     poetry run isort src test       build_tool.py:29
                    INFO     poetry run autoflake src test   build_tool.py:29
[03/25/24 22:21:33] INFO     poetry run black src test       build_tool.py:29
All done! ✨ 🍰 ✨
4 files left unchanged.
Testing...
                    INFO     poetry run pytest               build_tool.py:29
============================ test session starts =============================
platform linux -- Python 3.10.12, pytest-8.1.1, pluggy-1.4.0
rootdir: /home/greg/dev/poetry-slam
configfile: pytest.ini
plugins: cov-4.1.0
collected 5 items

test/test_slam.py .....                                                                                                                                                                                                                [100%]

---------- coverage: platform linux, python 3.10.12-final-0 ----------
Name                            Stmts   Miss  Cover   Missing
-------------------------------------------------------------
src/poetry_slam/__init__.py         0      0   100%
src/poetry_slam/build_tool.py      51      5    90%   38-40, 44, 48
src/poetry_slam/cli.py             37     37     0%   1-75
-------------------------------------------------------------
TOTAL                              88     42    52%

# ...and so on...
```
