# poetry-slam

An opinionated build tool for python poetry projects. poetry-slam saves me having to add optional dev dependencies and boilerplate build scripts to every project for things like tests, coverage, package installation, automatic formatting and &amp;c.

### What It Does
* installs isort, autoflake, and black
* adds pytest and pytest-cov as dev dependencies to your pyproject.toml (optional)
* adds opinionated defaults for isort, autoflake, black, pytest, and pytest-cov (optional)


## Installation

Clone the repository and install poetry-slam locally. You need the following prerequisites:

* python
* poetry


```bash
% git clone https://github.com/evilchili/poetry-slam.git
% cd poetry-slam
% poetry run slam build
% pip3 install dist/*.whl
```

## Basic Usage:

### Configuring Your Project

poetry-slam expects your package python source in `src/` and your tests in `test/`. 

You'll probably want this configuration in your pyproject.toml, but poetry-slam won't do this for you:

```toml
packages = [
    {include = "*", from = "src"},
]
```

### Initializing poetry-slam

The first time you use poetry-slam in a new project, it's a good idea to run `slam init`. This will add opinionated defaults for the build tooling directly to your pyproject.toml. 

```bash
% cd /some/poetry-project/
% slam init
Added poetry-slam defaults to pyproject.toml
% poetry update
```

### The Build Loop

The most common usage and the default if no command is specified is to do a `build`, which will:

* formats your source with isort, autoflake, and black;
* run all tests;
* (re)install the packages in your projet virtual environment; and 
* does a package release build

```bash
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

test/test_slam.py .....                                               [100%]

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
