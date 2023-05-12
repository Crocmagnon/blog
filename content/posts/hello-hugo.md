---
title: "Hello Hugo"
date: 2023-05-12T10:14:52+02:00
draft: false
# weight: 1
# aliases: ["/first"]
tags: ["initial", "hello"]

author: "Gabriel Augendre"
# author: ["Me", "You"] # multiple authors
showToc: true
TocOpen: false
hidemeta: false
comments: false
description: "Desc Text."
canonicalURL: "https://canonical.url/to/page"
disableShare: false
disableHLJS: false
hideSummary: false
searchHidden: true
ShowReadingTime: true
ShowBreadCrumbs: true
ShowPostNavLinks: true
ShowWordCount: true
ShowRssButtonInSectionTermList: true
UseHugoToc: true
cover:
    image: "<image path/url>" # image path/url
    alt: "<alt text>" # alt text
    caption: "<text>" # display caption under cover
    relative: false # when using page bundles set this to true
    hidden: true # only hide on current single page
    appendFilePath: true # to append file path to Edit link
---

## Hello world

This is an introduction post using **hugo**, a SSG written in *golang*.

```python
def hello(name: str = "World") -> str:
    return f"Hello, {name}"

if __name__ == "__main__":
    print(hello("Gabriel"))
```

```go
package main

import "fmt"

func main() {
    fmt.Println("Hello, world")
}
```

