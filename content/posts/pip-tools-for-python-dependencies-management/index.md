---
title: "pip-tools for Python dependencies management"
tags: ['dependencies', 'pip-tools', 'python']
date: 2023-03-02T13:07:26.381756+00:00
aliases: ["/pip-tools-for-python-dependencies-management"]
description: "Here's how and why I use pip-tools for my side-projects."
summary: "Here's how and why I use pip-tools for my side-projects."
---
## 📖 Story time

At the end of 2020, I wrote an article entitled [Poetry for Python dependencies management]({{< ref "poetry-python-dependencies-management" >}}). I described ITSF's requirements for a dependencies management system and how we found Poetry useful. After updating our internal projects, I tackled my side projects and moved them to Poetry.

The requirements from late 2020 were the following:

> * It must **manage transitive dependencies**[^transitive] for us. Developers should only have to specify the direct dependencies of their projects. Transitive dependencies and the exact versions to install must be defined by the tool.
> * Any **conflicts** in dependencies must prevent their installation and break the build.
> * Adding a dependency after the initial setup must check for **compatibility with existing direct and transitive dependencies**.
> * It must **fit into a Docker-based workflow** while still being **easy to use** in a development environment.
> * It must permit **reproducible builds**. We must be able to checkout the source code at a specific version and build the app as it was released this day with the exact same versions of all the packages.
> * It should have features for **building and publishing packages** on PyPI (or a private package registry).
> * Bonus point if it can export to the requirements.txt format for compatibility.

[^transitive]: A transitive dependency is the dependency of a dependency. For example, my app relies on the `requests` package for HTTP requests. This package relies on several others to do its job, like `certifi`, `chardet`, etc. These are transitive dependencies because my app doesn't rely directly on them.

At the time, we considered `pipenv`, `poetry` and `pip-tools`, and chose Poetry because it was the only one checking all the boxes.

Two years later, these requirements haven't changed, but I now find Poetry to be too complex and moved all my active side projects to `pip-tools`.

`pip-tools` regroups two utilities. The first generates a `requirements.txt` from a source, and the other takes the generated file and syncs the virtual environment to the described state. It fits well in the UNIX philosophy of one tool doing one thing and doing it well.

It doesn't try to manage your virtual environments, it doesn't try to build and publish packages... It just manages your dependencies.

## 👨🏻‍🔧 My new workflow

I'm using two source requirements files:

* `requirements.in` for the production dependencies
* `requirements-dev.in` for the development dependencies

Then, I use `pip-compile` to generate three files:

* `requirements.txt` for the production dependencies, generated from `requirements.in`
* `constraints.txt` for the constraints the production dependencies must impose on development dependencies, generated from `requirements.in`[^constraints]
* `requirements-dev.txt` for the development dependencies, generated from `requirements-dev.txt` and `constraints.txt`.

[^constraints]: I first used `requirements.txt` as the constraint file but I had some issues with extras. I now generate a separate `constraints.txt` file with `--strip-extras` to avoid this.

And finally `pip-sync` updates my virtualenv, adding missing packages and removing old ones.

### 📑 Samples

Here's what the source files look like for this blog:

```plain
# requirements.in
django[argon2]>=4.1,<5.0
django-cleanup>=6.0
django-environ>=0.9.0
# ...
```

```plain
# requirements-dev.in
-c constraints.txt
pre-commit>=2.7
pytest>=7.0
# ...
```

### 🪄 Invoke

The commands used to compile the three files are:

```shell
pip-compile -q --allow-unsafe --resolver=backtracking --generate-hashes requirements.in
pip-compile -q --allow-unsafe --resolver=backtracking --strip-extras -o constraints.txt requirements.in
pip-compile -q --allow-unsafe --resolver=backtracking --generate-hashes requirements-dev.in
```

This is a lot to remember and I have a terrible memory, so I'm using [invoke](https://www.pyinvoke.org/) to call the commands for me.

```python
# tasks.py
from pathlib import Path

from invoke import Context, task

BASE_DIR = Path(__file__).parent.resolve(strict=True)

@task
def update_dependencies(ctx: Context, *, sync: bool = True) -> None:
    return compile_dependencies(ctx, update=True, sync=sync)


@task
def compile_dependencies(
    ctx: Context, *, update: bool = False, sync: bool = False
) -> None:
    common_args = "-q --allow-unsafe --resolver=backtracking"
    if update:
        common_args += " --upgrade"
    with ctx.cd(BASE_DIR):
        ctx.run(
            f"pip-compile {common_args} --generate-hashes requirements.in",
            pty=True,
            echo=True,
        )
        ctx.run(
            f"pip-compile {common_args} --strip-extras -o constraints.txt requirements.in",
            pty=True,
            echo=True,
        )
        ctx.run(
            f"pip-compile {common_args} --generate-hashes requirements-dev.in",
            pty=True,
            echo=True,
        )
    if sync:
        sync_dependencies(ctx)


@task
def sync_dependencies(ctx: Context) -> None:
    with ctx.cd(BASE_DIR):
        ctx.run("pip-sync requirements.txt requirements-dev.txt", pty=True, echo=True)
```

Invoke is a sort of Makefile, but written in Python.

```shell-session
$ invoke --list  # shorter: inv -l
Available tasks:

  compile-dependencies
  sync-dependencies
  update-dependencies

$ inv compile-dependencies
# Runs the commands...
```

### 📦 Add/update dependencies

Now when I need to add a dependency, I first edit the relevant `*.in` file, then I run `inv compile-dependencies` to compile all the files without updating the existing dependencies and finally `inv sync-dependencies` to really install them locally (or shorter with `inv compile-dependencies -s`).

If I want to update my dependencies, a simple `inv update-dependencies` is all I need.

After that, I commit all the `*.in` and `*.txt` files so that my future self and other people can reproduce my build.

In other words:

```shell
echo "new_package>=1.2" >> requirements.in
inv compile-dependencies -s
git add *.in *.txt
git commit -m "Add new_package"
```

### 👀 Missing compilation?

In order to avoid forgetting to compile my dependencies, I added a few pre-commit hooks to my projects:

```yaml
repos:
  - repo: https://github.com/jazzband/pip-tools
    rev: 6.12.2
    hooks:
      - id: pip-compile
        name: pip-compile requirements.txt
        args: [-q, --allow-unsafe, --resolver=backtracking, --generate-hashes, requirements.in]
        files: ^requirements\.(in|txt)$
      - id: pip-compile
        name: pip-compile constraints.txt
        args: [-q, --allow-unsafe, --resolver=backtracking, --strip-extras, --output-file=constraints.txt, requirements.in]
        files: ^requirements\.in|constraints\.txt$
      - id: pip-compile
        name: pip-compile requirements-dev.txt
        args: [-q, --allow-unsafe, --resolver=backtracking, --generate-hashes, requirements-dev.in]
        files: ^requirements-dev\.(in|txt)$
```

These will run the `pip-compile` commands whenever the source or compiled files have changed to ensure the compiled files are up to date with the sources before committing. It won't update the dependencies though, as it's not desirable here.

## 🔀 Transition

Moving from Poetry to pip-tools was really easy since all the hard work was already done. I just took the dependencies listed in `pyproject.toml`, copied them over to the `*.in` files and compiled the `*.txt`

## 👨🏻‍💻 Developer experience

The beauty with all this is that I now have regular `requirements.txt` files that I can pass to `pip install -r`. It means potential collaborators don't need to worry about `pip-tools`. Or that I don't need yet another binary in my Docker images.

> *I can just rely on `pip`, and it's relaxing.*
