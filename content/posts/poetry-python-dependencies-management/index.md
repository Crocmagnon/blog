---
title: "Poetry for Python dependencies management"
tags: ['ITSF', 'dependencies', 'poetry', 'python']
date: 2020-12-30T20:44:05.549630+00:00
aliases: ["/poetry-python-dependencies-management"]
---
At [ITSF](https://itsf.io), teams using the same languages/frameworks regularly meet to share experience and decide on common guidelines. With the Python teams, we recently decided to change our dependencies management system to something more robust because we were not satisfied with `pip` alone.

## ✅ Requirements

Here's a list of the features we expected from our new tool:

* It must **manage transitive dependencies**[^transitive] for us. Developers should only have to specify the direct dependencies of their projects. Transitive dependencies and the exact versions to install must be defined by the tool.
* Any **conflicts** in dependencies must prevent their installation and break the build.
* Adding a dependency after the initial setup must check for **compatibility with existing direct and transitive dependencies**.
* It must **fit into a Docker-based workflow** while still being **easy to use** in a development environment.
* It must permit **reproducible builds**. We must be able to checkout the source code at a specific version and build the app as it was released this day with the exact same versions of all the packages.
* It should have features for **building and publishing packages** on PyPI (or in our case a private package registry).
* Bonus point if it can export to the requirements.txt format for compatibility.

[^transitive]: A transitive dependency is the dependency of a dependency. For example, my app relies on the `requests` package for HTTP requests. This package relies on several others to do its job, like `certifi`, `chardet`, etc. These are transitive dependencies because my app doesn't rely directly on them.

While `pip` can provide a semblance of builds reproducibility and can easily be used in a Docker-based workflow, at the time we did our research (sept. 2020) it did not fit the other use cases[^newpip].

[^newpip]: Since then, the team behind `pip` switched to a new dependency resolver. We did not research this further but it seems to solve the dependency conflicts issues. See [the blog post](https://pyfound.blogspot.com/2020/11/pip-20-3-new-resolver.html) introducing the new pip resolver.

Our main contenders were:

* [poetry](https://python-poetry.org/)
* [pipenv](https://pipenv.pypa.io/en/latest/)
* [pip-tools](https://pypi.org/project/pip-tools/)

Among them, only poetry ticks all the boxes. pip-tools and pipenv don't have features for publishing packages, but based on our research they seemed to provide all the other features we required.

## ⚙️ Poetry

### Version constraints

![Poetry logo](35.svg)


Poetry lets you specify your direct dependencies in a standard file called `pyproject.toml`. You can either edit this file manually or use the `poetry` command line tool.

After specifying your dependencies, you need to `lock` them. The locking phase is a crucial part of the workflow because that's when poetry decides which version of each package it needs to install. It does that on its own and breaks if there are incompatible dependencies in your tree. It generates a file called `poetry.lock` which is meant to be checked in your VCS so that other developers get this file when checking out the project.

When installing dependencies, poetry will read the lock file and install the locked versions of the packages.

This workflow allows you to specify your real dependencies in `pyproject.toml`, with non-strict version constraints like `django = "^3.1"`. This specific example specifies that we rely on `django`, at least in version `3.1` but we accept any upgrade up to version `4.0`. There are other version constraints you can use, they are documented [here](https://python-poetry.org/docs/versions/).

When you add a new package to your dependencies list, poetry automatically checks for dependencies compatibility and breaks if there is a clash. Adding a new package doesn't update all your existing pinned dependencies.

### Using a private registry

Poetry makes it very easy to use a private registry to fetch packages that you may have built and distributed internally. Instead of having to create a file somewhere in the virtualenv on every machine you need to access the said registry, you just need to add your registries in the `pyproject.toml`. Since this file is checked into your VCS, all of your developers and all of your build environment will have the configuration they need out of the box.

```toml
[[tool.poetry.source]]
name = "pypi-mirror"
url = "https://devpi.example.com/root/pypi/+simple/"
default = true
[[tool.poetry.source]]
name = "internal"
url = "https://devpi.example.com/root/internal/+simple/"
secondary = true
```

### Publishing packages

Building and publishing a package can be done in a single command:

```bash
poetry publish --build -r internal -u username -p password
```

You don't need to go through a complicated configuration process: all the configuration is available in a committed file.

## 🔀 Transition

Transitioning to poetry is easy but requires some manual work if you want to get the full benefits. Indeed, you need to extract your direct dependencies from the requirements.txt you already have. If they are documented somewhere, well you're in luck. If not, you need to spend some time to properly extract them.

To help me in this task, I used `pipdeptree`. After installing it in the virtualenv with all the dependencies, I ran the CLI tool. It renders the installed packages in a tree, like so:

```
model-bakery==1.2.1
  - django [required: >=1.11.0<3.2, installed: 3.1.4]
    - asgiref [required: >=3.2.10,<4, installed: 3.3.1]
    - pytz [required: Any, installed: 2020.5]
    - sqlparse [required: >=0.2.2, installed: 0.4.1]
pipdeptree==2.0.0
  - pip [required: >=6.0.0, installed: 20.2.2]
pre-commit==2.9.3
  - cfgv [required: >=2.0.0, installed: 3.2.0]
  - identify [required: >=1.0.0, installed: 1.5.10]
  - nodeenv [required: >=0.11.1, installed: 1.5.0]
  - pyyaml [required: >=5.1, installed: 5.3.1]
  - toml [required: Any, installed: 0.10.2]
  - virtualenv [required: >=20.0.8, installed: 20.2.2]
    - appdirs [required: >=1.4.3,<2, installed: 1.4.4]
    - distlib [required: >=0.3.1,<1, installed: 0.3.1]
    - filelock [required: >=3.0.0,<4, installed: 3.0.12]
    - six [required: >=1.9.0,<2, installed: 1.15.0]
```

Unfortunately, it sometimes marks some packages as transitive dependencies when you really need them listed as direct dependencies. In my experience, it was often the case for `requests`, which other packages also rely upon. Therefore, you can't trust it blindly, hence the manual work.

## 🧑‍💻 Developer experience

I've been personally very satisfied with this transition to poetry on the projects I maintain. It was a bit of work to make the switch but so far I've only been enjoying benefits.

The setup in a Docker image is also quite straightforward if you accept to have poetry in your final image. If you prefer to have lightweight images, you can use multi-stage builds to install your dependencies in a first stage and retrieve the virtualenv containing only your project's dependencies in a later one. If you're interested, check out [this article]({{< ref "lighten-your-python-image-docker-multi-stage-builds" >}}) I wrote on the subject!

## 🗒 Closing thoughts

Poetry is very **pleasant** to work with and we feel **safer** adding dependencies, knowing that there won't be any surprise conflict after the installation. We can also easily **build and publish** packages for internal use with the same tool, it's just a new command to learn.

Anyway, I hope you learned something in this post about our experience with poetry! As always, please [contact me]({{< ref "about-me#contact" >}}) if you have comments or questions!
