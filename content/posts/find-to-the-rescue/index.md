---
title: "find to the rescue"
date: 2023-06-29T22:37:30+02:00
tags: [find, ubuntu, unix, posix, command line, terminal]

description: "Helps you locate files matching criteria"
summary: "find has many filters to help you locate the files you're looking for."
---

`find` is a cool piece of software.
It basically helps you find (didn't see that coming, huh?) files matching criteria.

## 🕵🏻‍♂️ Basic filters
One of the most common criteria is `-name`.
You're looking for a file, but you only remember parts of its name? `find` to the rescue!

```shell
find . -name "foo*"
find . -name "*bar*"
find . -name "*.baz"
```

You want to discover the files modified in the last five minutes?

```shell
find . -mmin -5
```

This recently helped me discover what files Ubuntu created when setting up a keyring, in order to automate the deployment of desktop machines.

{{< note class="info" title="Different implementations" >}}
There are [differences](https://unix.stackexchange.com/questions/475020/difference-between-find-and-gnu-find) between implementations present in GNU/Linux and other systems, so your mileage may vary. The commands present in this article work on macOS.
{{</note>}}

## 🚜 Executing actions & deleting
Filters can be combined and a special `-exec` filter allows you to create entirely rules.
It also runs the command on all files, helping you run actions instead of filtering if that's what you're after.

E.g. count the lines of all markdown files with a modification date **older** than 5 days:

```shell
find . -mtime +5 -type f -name "*.md" -exec wc -l {} +
```

Special `-exec` rules:

* `{}` is used as a placeholder: the file names will be placed at this position in the command execution.
* the statement must be terminated by either `\;` or `+`
  * `\;` will apply the command to a single file at a time
  * `+` will apply the command to all files at the same time

The escaping before the semicolon is necessary, otherwise shells would interpret it as the end of the command and `find` would complain about the missing character.

Since deleting is a common action, it has its own flag:

```shell
find . -name "*.pyc" -delete
```

## 📚 Further reading

I don't think I ever had to use any more filters, but there are a lot more!
I don't intend on covering them all here, especially since I don't know half of them. RTFM!

```shell
tldr find
man find
```
