---
title: "How to use pipx with pyenv"
tags: ['pipx', 'pyenv', 'python']
date: 2020-12-30T08:40:58.362871+00:00
---
## 👨🏻‍💻 TL;DR

In my case with `fish` I added this line to my `config.fish`:

```fish
set -gx PIPX_DEFAULT_PYTHON "$HOME/.pyenv/versions/3.8.5/bin/python"
```

It's roughly the bash equivalent for

```bash
export PIPX_DEFAULT_PYTHON="$HOME/.pyenv/versions/3.8.5/bin/python"
```

## 📖 Backstory

As a Python developer, my workflow often involves running multiple versions of Python on different projects. To help me in this task, I use [`pyenv`](https://github.com/pyenv/pyenv) which is a wonderful tool to easily install and manage multiple Python versions on your system.

I also have a Python version installed via [Homebrew][brew] for some formulae that require it. This version is the default for any script if pyenv doesn't specify any version.

[brew]: https://brew.sh/

Finally, I also use [`pipx`](https://pipxproject.github.io/pipx/) which allows me to install python packages in their own virtual environment without messing with my system installation and still have them ready for use on the command line.

My problem is that `pipx` will by default use the Python version provided by Homebrew to install the executables. As I keep my system up to date with Homebrew, the Python version often updates. When that happens, all of my `pipx` packages break and I have to reinstall them all. Granted, `pipx` provides a command to do that easily but I'd still like to avoid the operation.

Thankfully, as [documented](https://pipxproject.github.io/pipx/docs/)[^1], `pipx` supports an environment variable called `PIPX_DEFAULT_PYTHON`. You just need to point it to your preferred Python interpreter and be done with it!

[^1]: Also available when running `pipx --help`

!!! info "Update"
    I've now [switched](/setup-rtx-with-direnv-for-python/) from `pyenv` to `rtx` but the concept remains the same: install python with `rtx`, then set `PIPX_DEFAULT_PYTHON`.
