---
title: "Demo post"
tags: []
date: 2021-01-03T18:08:52.170212+00:00
---
This is a paragraph and should look like it. It is probably left align, not justified. After all, we're on the web not in a book.

[TOC]

# Heading 1
## Heading 2
### Heading 3
#### Heading 4
##### Heading 5
###### Heading 6

This is a [link](#).

Here's an abbreviation: HTML.

*[HTML]: Hyper Text Markup Language

Here's a button

[<button>Button</button>](#)

* **Bold text**
* *Italic text*
*  <u>Underlined text</u>
*  <mark>Highlighted text</mark>
*  <code>Inline code</code>
*  <kbd>Alt</kbd> + <kbd>F4</kbd>

!!! info "Info"
    This is an info admonition.

!!! success "Success"
    This is a success admonition.

!!! warning "Warning"
    This is a warning admonition.

!!! danger "Danger"
    This is a danger admonition.

```python hl_lines="1 3"
# main.py

def main():
    print("Hello world")

if __name__ == "__main__":
    main()
```

* Unordered
* list
* of items

Breaking paragraph

1. Ordered
2. list
2. of items

> *This quote was told by someone very famous.*
>
> \- Somewone very famous

This should be an image:

![Image alt text](/attachments/32/processed/)

<details>
  <summary>Spoiler alert!</summary>
  <p>Some text. 🙂</p>
</details>

| Heading 1 | Heading 2 |
|-----------|-----------|
| Table item 1 | Table item 2 |
| Table item 1 | Table item 2 |
| Table item 1 | Table item 2 |
| Table item 1 | Table item 2 |

Now onto a somewhat real example:

Notice the second `FROM` instruction? It tells Docker to start again from a new image, like at the beginning of a build, except that it will have access to the last layers of all the previous stages.

Then, the `COPY --from` is used to retrieve the built binary from the first stage.

In this extreme case, the final image weighs nothing more than the binary itself since `scratch` is a special empty image with no operating system.

Link to another section: [link](#python_poetry)

## 🐍 Applying to Python & Poetry {: id="python_poetry" }
### Install the dependencies

Let's start with a basic Dockerfile with a single stage that will just install this blog's dependencies and run the project.[^blog]

[^blog]: The source code is available [on sourcehut](https://git.augendre.info/gaugendre/blog).

Basically a multi-stage build allows you to sequentially use multiple images in one Dockerfile and pass data between them.

This is especially useful for projects in statically compiled languages such as Go, in which the output is a completely standalone binary: you can use an image containing the Go toolchain to build your project and copy your binary to a barebones image to distribute it.
