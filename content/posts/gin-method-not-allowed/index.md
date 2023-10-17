---
title: "Gin Method Not Allowed"
date: 2023-10-17T18:29:45+02:00
draft: false
tags: ["go", "gin", "golang", "http", "ovh", "ovhcloud"]

# Keep them short
description: "By default `gin` returns a 404 for an incorrect HTTP verb sent to a handled path. This can be fixed."
summary: "By default `gin` returns a 404 for an incorrect HTTP verb sent to a handled path. This can be fixed."

cover:
  image: "gin.jpg"
  relative: true
  alt: "Gin & Tonic"
  caption: 'Gin & Tonic from Vlad Tchompalov sur (Unsplash)'
  hidden: false  # applies only on single view

# showToc: true
# TocOpen: false
---

TL;DR: by default `gin` returns a 404 for an incorrect HTTP verb sent to a handled path. Double-check the method you're using.

## 📖 Context
At OVHcloud, we use [`gin-gonic/gin`](https://github.com/gin-gonic/gin) as the go-to HTTP web framework for our internal services.

The default behavior when receiving a request for a path that's handled but with an incorrect HTTP verb is to reply with `404 Not Found`. 
That's confusing because this status code is more often used when a path is not handled at all.

{{< highlight go "linenos=inline" >}}
package main

import "github.com/gin-gonic/gin"

func main() {
	router := gin.Default()
	router.GET("/hello", func(c *gin.Context) {
		c.JSON(http.StatusOK, gin.H{"hello": "gin"})
	})
	router.Run("localhost:8080")
}
{{< /highlight >}}

```shell
$ # existing path
$ curl -i http://localhost:8080/foo
HTTP/1.1 200 OK
Content-Type: application/json; charset=utf-8
Date: Tue, 17 Oct 2023 15:59:49 GMT
Content-Length: 15

{"hello":"gin"}⏎

$ # wrong method
$ curl -i -X POST http://localhost:8080/foo
HTTP/1.1 404 Not Found
Content-Type: text/plain
Date: Tue, 17 Oct 2023 16:00:03 GMT
Content-Length: 18

404 page not found⏎

$ # non-existent path
$ curl -i http://localhost:8080/bar
HTTP/1.1 404 Not Found
Content-Type: text/plain
Date: Tue, 17 Oct 2023 16:00:17 GMT
Content-Length: 18

404 page not found⏎
```

## 👨🏻‍🔧 Fixing the issue
The router can be configured to handle these cases, but it needs to be manually enabled:

{{< highlight go "linenos=inline,hl_lines=7" >}}
package main

import "github.com/gin-gonic/gin"

func main() {
	router := gin.Default()
	router.HandleMethodNotAllowed = true
	router.GET("/hello", func(c *gin.Context) {
		c.JSON(http.StatusOK, gin.H{"hello": "gin"})
	})
	router.Run("localhost:8080")
}
{{< /highlight >}}

```shell
$ # wrong method
$ curl -i -X POST http://localhost:8080/foo
HTTP/1.1 405 Method Not Allowed
Content-Type: text/plain
Date: Tue, 17 Oct 2023 16:00:53 GMT
Content-Length: 22

405 method not allowed⏎
```

As far as I can tell, this boolean isn't documented on the [docs website](https://gin-gonic.com/docs/), but it has a [doc comment](https://github.com/gin-gonic/gin/blob/a481ee2897af1e368de5c919fbeb21b89aa26fc7/gin.go#L105-L111) attached.

## 👀 Going further
As you can see, the response still misses the `Allow` header that should document the allowed methods on the endpoint.

A PR was opened in 2020 to fix this and maintainers seemed OK to merge it, but it had conflicts and the original author wasn't responsive ;
so I opened [a new one](https://github.com/gin-gonic/gin/pull/3759). I hope it will get merged soon!
