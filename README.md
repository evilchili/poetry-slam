# poetry-slam

An opinionated build tool for python poetry projects. poetry-slam saves me having to add optional dev dependencies and boilerplate build scripts to every project for things like tests, coverage, package installation, automatic formatting and &amp;c.

### What It Does
* installs isort, autoflake, and black
* adds pytest and pytest-cov as dev dependencies to your `pyproject.toml` (optional)
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

## Starting a New Project

poetry-slam can generate a boilerplate python project with a cli:

```bash
% mkdir /tmp/test_project
% cd /tmp/test_project
% git init
Initialized empty Git repository in /tmp/test_project/.git/

% slam new test_project
Added poetry-slam defaults to pyproject.toml
Formatting...
Installing...
Testing...
========== test session starts ==========
platform linux -- Python 3.10.12, pytest-8.1.1, pluggy-1.4.0
rootdir: /tmp/test_project
configfile: pyproject.toml
plugins: cov-5.0.0
collected 1 item                                                                                                                                                                                                                             

test/test_test_project.py x                                     [100%]
test/test_test_project_cli.py x                                 [100%]

---------- coverage: platform linux, python 3.10.12-final-0 ----------
Name                           Stmts   Miss  Cover   Missing
------------------------------------------------------------
src/test_project/__init__.py       0      0   100%
src/test_project/cli.py           23      9    61%   37-50, 57
------------------------------------------------------------
TOTAL                             23      9    61%


========== 2 xfailed in 0.11s ==========
Building...
slam build: SUCCESS
Successfully initialized new default project test_project.
```


## Configuring An Existing Project

poetry-slam expects your package python source in `src/` and your tests in `test/`. 

You'll probably want this configuration in your `pyproject.toml`, but poetry-slam won't do this for you:

```toml
packages = [
    {include = "*", from = "src"},
]
```

#### Initializing poetry-slam

The first time you use poetry-slam in a new project, it's a good idea to run `slam init`. This will add opinionated defaults for the build tooling directly to your `pyproject.toml`. It will also add both pytest and pytest-cov as dependencies in your dev group.

```bash
% cd /some/poetry-project/
% slam init
Added poetry-slam defaults to pyproject.toml
% poetry update
```

#### What You Don't Need

Aside from pytest and pytest-cov, which poetry-slam will add for you, You don't need other dependencies in your project's dev group. When you install poetry-slam you will also get isort and friends if they aren't already present, and these tools will automatically load configuration from the first `pyproject.toml` they find in your directory hierarchy.

You also don't need tool-specific configuration files or global defaults, since the configs are added directly to your `pyproject.toml`.


### The Build Loop

The most common usage and the default if no command is specified is to do a `build`, which will:

* format your source with isort, autoflake, and black;
* run all tests;
* (re)install the packages in your project virtual environment; and 
* build a release in `dist/`.

```bash
% slam
Formatting...
Testing...
Installing...
Building...
slam build: SUCCESS
```

You can also run individual steps; see `slam --help` for details:

```bash
% slam --help

 Usage: slam [OPTIONS] COMMAND [ARGS]...

╭─ Options ──────────────────────────────────────────────────────────────────────╮
│ --verbose               --no-verbose          Enable verbose output.           │
│                                               [default: no-verbose]            │
│ --log-level                             TEXT  Set the log level.               │
│                                               [default: error]                 │
│ --poetry                                PATH  Path to the poetry executable;   │
│                                               defaults to the first in your    │
│                                               path.                            │
│                                               [default: poetry]                │
│ --install-completion                          Install completion for the       │
│                                               current shell.                   │
│ --show-completion                             Show completion for the current  │
│                                               shell, to copy it or customize   │
│                                               the installation.                │
│ --help                                        Show this message and exit.      │
╰────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ─────────────────────────────────────────────────────────────────────╮
│ build     Calls format, test, and install before invoking 'poetry build'.      │
│ format    Run isort, autoflake, and black on the src/ and test/ directories.   │
│ init      Add opinionated defaults to your pyproject.toml.                     │
│ install   Synonym for 'poetry install'                                         │
│ test      Synonym for 'poetry run pytest' Output is always verbose.            │
╰────────────────────────────────────────────────────────────────────────────────╯

```

## Testing With Pytest

Anything passed to `slam test` will be passed directly to pytest as command-line arguments. So for example:

```bash
% slam test -vv -k test_this_one_thing
```


## Debugging

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

## Overriding the Defaults

Why would you do that? Clearly my opinions are the best opinions. :D

...but if you want to be wrong, run `slam init` and then modify the generated configuration to your liking. So long as you don't remove the slam comment:

```
### SLAM
```

running `slam init` again will not override your changes.
