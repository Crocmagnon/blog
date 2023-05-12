---
title: "Automate bug findings with git"
tags: ['bisect', 'bugs', 'git']
date: 2021-12-22T22:08:07.191735+00:00
aliases: ["/automate-bug-findings-with-git"]
---
## 🔍 Git bisect

When you're trying to troubleshoot a bug, finding the original commit is often helpful as it gives you context.

Enters `git bisect`! If you haven't already, consider taking a short detour to the [documentation](https://git-scm.com/docs/git-bisect).

> This command uses a binary search algorithm to find which commit in your project's history introduced a bug.

## 🤙 The manual way

`git bisect` works by taking a "good" commit and a "bad" one and from there it will checkout a commit in between. Then, you check if your bug is still present and tell git about it. It then repeats this process, narrowing down its search until it finds the first "bad" commit.

Manually checking the presence of the bug may be tedious if the process is involved or if there's a very large number of commits to go through.

## 🤖 Automating it for fun and profit

If you know how to script the detection of the bug, let's say you can reproduce it in a unit test, then you can use the `run` subcommand.

It takes a command that should exit with 0 if the commit is good and anything else if it's bad. Conveniently, most test runners behave this way, so you should be able to use the tools you already know.

Git will then do all the heavy lifting for you, running your test script after each checkout and swiftly find the culprit.

!!! Info "☝️ Pro tip"
    If the script you want to run is versioned, then when git checks out previous commits your test script might change.

    In order to avoid that, a possible workaround is to run a non-versioned copy of the script so it's not changed when git switches to an earlier version of your repository.
