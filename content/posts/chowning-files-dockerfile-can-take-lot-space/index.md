---
title: "Chowning files can take a lot of space in a Docker image"
tags: ['Docker', 'ITSF', 'chown', 'history', 'layer', 'multi-stage builds']
date: 2021-03-02T16:21:06.172437+00:00
aliases: ["/chowning-files-dockerfile-can-take-lot-space"]
canonicalURL: "/chowning-files-dockerfile-can-take-lot-space"
---
Today I learned that recursively changing the owner of a directory tree in a Dockerfile can result in some serious increase in image size.

## 🚛 The issue
You may remember how in a [previous post]({{< ref "docker-images-layers-and-cache/" >}}) we used a small example to discuss layers and final image size. Well, here's our example again, slightly modified.

```Dockerfile {hl_lines="5"}
# Dockerfile
FROM ubuntu
WORKDIR /app
RUN fallocate -l 100M example
RUN chown 33:33 example
```

Given that the base image weighs ~75MB, we could expect the final image to weigh ~175MB (~75 from the base image + ~100 from the big file we generated).

It turns out that since `chown`ing the file modifies it, the `example` file will count twice: once in the `fallocate` layer, and once in the `chown` layer, resulting in an image size of ~275MB.

## 📉 Workaround
Since creating "large" amounts of data in a Docker image can be quite common (think about dependencies, static files, etc), I guess that workaround strategies are required. Fortunately, our backs are covered.

Let's take a slightly more complex example to illustrate some real life situations you might encounter:

```Dockerfile
FROM ubuntu AS build
WORKDIR /build
RUN fallocate -l 100M binary

FROM ubuntu
WORKDIR /app
RUN fallocate -l 100M example
COPY --from=build /build/binary /app/binary
RUN chown -R 33:33 /app
```

This results in an image weighing 492MB. Let's bring it down to 283MB! (2x~100MB + ~75MB)

```Dockerfile {hl_lines="9 14 15 19"}
FROM ubuntu AS build
WORKDIR /build
RUN fallocate -l 100M binary

FROM ubuntu
WORKDIR /app

# /app is empty so only the folder is modified.
RUN chown -R 33:33 /app

# Running these in the same step prevents docker
# from generating an intermediate layer with the
# wrong permissions and taking precious space.
RUN fallocate -l 100M example \
	&& chown 33:33 example

# Using --chown with COPY or ADD copies the files
# with the right permissions in a single step.
COPY --chown=33:33 --from=build /build/binary /app/binary
```

There you go! By being smart about when to run the permission changes, we just saved ourselves 200MB of disk space and network bandwidth. That's about 60% for this specific image!

In the specific case I was investigating at [ITSF](https://itsf.io), the image went from ~1.6GB to ~0.95GB just from this `chown` trick. We were copying a bunch of files in a directory and at the end we chowned the whole directory recursively. That directory weighed about 650MB, which counted twice in the final image size.

{{< note class="info" title="Info" >}}
Of course this also works with "simple" `COPY` and `ADD` instructions. It's not reserved to copying files from other stages.
{{< /note >}}

## 📓 Don't forget history!
I discovered that the `chown` was taking that much space using the underrated `docker history` command. I already briefly [introduced]({{< ref "docker-images-layers-and-cache/#cache-invalidation" >}}) it previously but now felt like a good time to remind you of its existence 🙂

Running it with our big 492MB image, here's the output:

```
$ docker history fat-image

IMAGE          CREATED          CREATED BY                                      SIZE      COMMENT
ec7efd2f2855   20 minutes ago   /bin/sh -c chown -R 33:33 /app                  210MB
562cdd7db0dd   21 minutes ago   /bin/sh -c #(nop) COPY file:3de744e61c00e7ca…   105MB
e2b74aa6952e   30 minutes ago   /bin/sh -c fallocate -l 100M example            105MB
8637829f8e9b   2 months ago     /bin/sh -c #(nop) WORKDIR /app                  0B
f643c72bc252   3 months ago     /bin/sh -c #(nop)  CMD ["/bin/bash"]            0B
<missing>      3 months ago     /bin/sh -c mkdir -p /run/systemd && echo 'do…   7B
<missing>      3 months ago     /bin/sh -c [ -z "$(apt-get indextargets)" ]     0B
<missing>      3 months ago     /bin/sh -c set -xe   && echo '#!/bin/sh' > /…   811B
<missing>      3 months ago     /bin/sh -c #(nop) ADD file:4f15c4475fbafb3fe…   72.9MB
```

All the `<missing>` rows plus the first row with a real ID above (`f643c72bc252`) are the layers of the base image. All the layers above are the ones that compose our image. We can clearly see that the `chown` layer weighs 210MB by itself.

That wraps it up for today! As always, I hope you learned something along the way 😊
