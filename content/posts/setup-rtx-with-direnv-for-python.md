---
title: "Setup rtx with direnv for Python"
tags: ['development', 'python', 'shell', 'virtualenv']
date: 2023-02-28T23:58:39.540937+00:00
---
## 👨🏻‍💻 TL;DR

```shell
## install rtx
brew install rtx direnv

## configure rtx & direnv
echo "direnv hook fish | source" >> ~/.config/fish/config.fish
# don't enable rtx's hook because it doesn't work well with direnv's python layout
# see https://github.com/jdxcode/rtx/discussions/235#discussioncomment-5159938

mkdir -p ~/.config/direnv/lib/
rtx direnv activate > ~/.config/direnv/lib/use_rtx.sh
echo "use rtx" > ~/.config/direnv/direnvrc
touch ~/.envrc

## Project setup
mkdir top-secret-project
cd top-secret-project
echo "python 3.11.1" > .tool-versions
rtx install
echo "layout python3" > .envrc
echo ".direnv" >> .gitignore
direnv allow
```

These are the latest versions of both tools, at the time of writing:
```plain
❯ direnv --version
2.32.2
❯ rtx --version
1.19.0 macos-arm64 (built 2023-02-28)
```

## 📖 Context
I was happily using [fish shell](https://fishshell.com/), Python, [direnv](https://direnv.net/), [pyenv](https://github.com/pyenv/pyenv) and [pyenv-virtualenv](https://github.com/pyenv/pyenv-virtualenv) to manage my projects and local Python versions. I heard about [asdf](https://asdf-vm.com/) in the past but didn't feel the need to change my tooling because I mainly work on Python-only projects.

Pyenv uses **shims**, which are a problem because when running `which <program>` you get a path to a **wrapper script** and not the real binary. It also means that binaries installed in one virtualenv are globally "accessible" (because the shims are always in your PATH) but when you try to run them you get an error asking you to activate the proper virtualenv.

My requirements for a new tool are the following:

* The tool MUST be globally available ;
* The tool SHOULD provide globally available versions of Python (and other tools like node as a bonus) ;
* I MUST be able to manage the Python version per project (and other tools like node as a bonus) ;
* The virtualenv MUST activate itself when I `cd` into the project's directory ;
* The tool MUST play nice with `direnv`.

pyenv already does all of this but:

* It adds a noticeable delay when opening a new shell ;
* It adds delay when calling shimed binaries (python, but also any other binary installed in a venv) ;
* It uses shims, which as explained above don't provide a great `which` experience.

I was watching [this YouTube video](https://www.youtube.com/watch?v=dFkGNe4oaKk) and the host mentioned a newcomer called `rtx`. It promises to be a drop-in replacement to `asdf` but written in Rust and doesn't used shims, so that's what I'm currently trying.

As I didn't find proper & clear setup instructions in the documentation, I wrote this post.

## 🏅 Achievements & improvements

* My shell startup time is noticeably reduced
* I don't have virtualenv binaries polluting my global PATH anymore
* All requirements are satisfied, except for the globally available tools
* I can now manage other language tooling with this setup
* I don't have to manually setup my virtualenv anymore, direnv does it for me

On the other hand, my tools are only available under `$HOME`. Since that's where I normally work, I'm ok with this limitation for now.

That's a clear win ! I'll keep using `rtx` and update this post if I find anything to complain about.
