---
title: "Docker images layers and cache"
tags: ['Docker', 'cache', 'layer']
date: 2020-12-28T07:55:41.393608+00:00
aliases: ["/docker-images-layers-and-cache"]
---
In this post, we'll walk through Docker image layers and the caching around them from the point of view of a Docker user. I'll assume you're already familiar with Dockerfiles and Docker concepts in general.

![Docker logo](32.png)

## ✌️ The two axioms of Docker layers
There are two key concepts to understand, from which everything else is deduced. Let's call them our axioms.

Axiom 1
: Every instruction in a Dockerfile results in a layer[^1]. Each layer is stacked onto the previous one and depends upon it.

Axiom 2
: Layers are cached and this cache is invalidated whenever the layer or its parent change. The cache is reused on subsequent builds.

[^1]: Well, that's not true anymore, see [Best practices for writing Dockerfiles: Minimize the number of layers (Docker docs)](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/#minimize-the-number-of-layers). But since it's easier to understand this way, I'm willing to make this compromise for this article.

So, what happens when we build a small Docker image?

```Dockerfile
# Dockerfile
FROM ubuntu
WORKDIR /app
COPY somefile ./
RUN md5sum somefile > somefile.md5
```

```text
$ echo "helloworld" > somefile
$ docker build -t gabnotes-example .

Sending build context to Docker daemon  3.072kB
Step 1/4 : FROM ubuntu
latest: Pulling from library/ubuntu
da7391352a9b: Pull complete
14428a6d4bcd: Pull complete
2c2d948710f2: Pull complete
Digest: sha256:c95a8e48bf88e9849f3e0f723d9f49fa12c5a00cfc6e60d2bc99d87555295e4c
Status: Downloaded newer image for ubuntu:latest
 ---> f643c72bc252
Step 2/4 : WORKDIR /app
 ---> Running in 0d58fcc66d8d
Removing intermediate container 0d58fcc66d8d
 ---> 8637829f8e9b
Step 3/4 : COPY somefile ./
 ---> 5edc5d0aab9d
Step 4/4 : RUN md5sum somefile > somefile.md5
 ---> Running in 8c54bb3e4453
Removing intermediate container 8c54bb3e4453
 ---> c2d34241963a
Successfully built c2d34241963a
Successfully tagged gabnotes-example:latest
```

1. Docker first downloads our base image since it doesn't exist in the local registry.
2. It creates the `/app` directory. Subsequent commands will run inside this directory.
3. It copies the file from our local directory to the image.
4. It stores the MD5 hash of our file inside a file named `somefile.md5`.

Now if we try to build the image again, without changing anything, here's what happens:

```text
$ docker build -t gabnotes-example .

Sending build context to Docker daemon  3.072kB
Step 1/4 : FROM ubuntu
 ---> f643c72bc252
Step 2/4 : WORKDIR /app
 ---> Using cache
 ---> 8637829f8e9b
Step 3/4 : COPY somefile ./
 ---> Using cache
 ---> 5edc5d0aab9d
Step 4/4 : RUN md5sum somefile > somefile.md5
 ---> Using cache
 ---> c2d34241963a
Successfully built c2d34241963a
Successfully tagged gabnotes-example:latest
```

For every step, Docker says it's "using cache." Remember our axioms? Well, each step of our first build generated a layer which is cached locally and was reused for our second build.

## 🔄 Cache invalidation

We can get some information about the layers of our image using `docker history`:

```text
$ docker history gabnotes-example

IMAGE          CREATED          CREATED BY                                      SIZE      COMMENT
c2d34241963a   23 minutes ago   /bin/sh -c md5sum somefile > somefile.md5       43B
5edc5d0aab9d   23 minutes ago   /bin/sh -c #(nop) COPY file:b87a7968d4d0a6b7…   11B
8637829f8e9b   23 minutes ago   /bin/sh -c #(nop) WORKDIR /app                  0B
f643c72bc252   4 weeks ago      /bin/sh -c #(nop)  CMD ["/bin/bash"]            0B
<missing>      4 weeks ago      /bin/sh -c mkdir -p /run/systemd && echo 'do…   7B
<missing>      4 weeks ago      /bin/sh -c [ -z "$(apt-get indextargets)" ]     0B
<missing>      4 weeks ago      /bin/sh -c set -xe   && echo '#!/bin/sh' > /…   811B
<missing>      4 weeks ago      /bin/sh -c #(nop) ADD file:4f15c4475fbafb3fe…   72.9MB
```

This output should be read as a stack: the first layer is at the bottom and the last layer of the image is at the top. This illustrates the dependencies between layers: if a "foundation" layer changes, Docker has to rebuild it and all the layers that were built upon.

It's natural: your layers 2 and 3 may depend on the output of the layer 1, so they should be rebuilt when layer 1 changes.

In our example:

```Dockerfile
# Dockerfile
FROM ubuntu
WORKDIR /app
COPY somefile ./
RUN md5sum somefile > somefile.md5
```

* the `COPY` instruction depends on the previous layer because if the working directory were to change, we would need to change the location of the file.
* the `RUN` instruction must be replayed if the file changes or if the working directory changes because then the output file would be placed elsewhere. It also depends on the presence of the `md5sum` command, which exists in the `ubuntu` image but might not exist in another one.

So if we change the content of `somefile`, the `COPY` will be replayed as well as the `RUN`. If after that we change the `WORKDIR`, it will be replayed as well as the other two.[^docs]

[^docs]: Read more about how Docker detects when the cache should be invalidated: [Leverage build cache](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/#leverage-build-cache)

Let's try this:

```text
$ echo "good bye world" > somefile
$ docker build -t gabnotes-example .

Sending build context to Docker daemon  3.072kB
Step 1/4 : FROM ubuntu
 ---> f643c72bc252
Step 2/4 : WORKDIR /app
 ---> Using cache
 ---> 8637829f8e9b
Step 3/4 : COPY somefile ./
 ---> ba3ed4869a32
Step 4/4 : RUN md5sum somefile > somefile.md5
 ---> Running in c66d26f47038
Removing intermediate container c66d26f47038
 ---> c10782060ad4
Successfully built c10782060ad4
Successfully tagged gabnotes-example:latest
```

See, Docker detected that our file had changed, so it ran the copy again as well as the `md5sum` but used the `WORKDIR` from the cache.

This mechanism is especially useful for builds that take time, like installing your app's dependencies.

## 🏃‍♂️ Speed up your builds

Let's consider another example:

```text
# requirements.txt
requests==2.25.1
```
```python
# main.py
import requests

res = requests.get("https://httpbin.org/get")
print(res.json())
```
```Dockerfile
# Dockerfile
FROM python:3.8.6-buster
WORKDIR /app
COPY . ./
RUN pip install -r requirements.txt
CMD ["python", "main.py"]
```

Let's build this.

```text
$ docker build -t gabnotes-example2 .

Sending build context to Docker daemon  4.096kB
Step 1/5 : FROM python:3.8.6-buster
3.8.6-buster: Pulling from library/python
Digest: sha256:6a25504ef508896ab6682c1696b53ea7a5247b45ca1466e708717ce675831c03
Status: Downloaded newer image for python:3.8.6-buster
 ---> d1bfb3dd9268
Step 2/5 : WORKDIR /app
 ---> Running in b07bbed274c2
Removing intermediate container b07bbed274c2
 ---> 21cbb4d03bf2
Step 3/5 : COPY . ./
 ---> 0cf5413cb6a1
Step 4/5 : RUN pip install -r requirements.txt
 ---> Running in 50147c21a8fa
Collecting requests==2.25.1
  Downloading requests-2.25.1-py2.py3-none-any.whl (61 kB)
Collecting certifi>=2017.4.17
  Downloading certifi-2020.12.5-py2.py3-none-any.whl (147 kB)
Collecting chardet<5,>=3.0.2
  Downloading chardet-4.0.0-py2.py3-none-any.whl (178 kB)
Collecting idna<3,>=2.5
  Downloading idna-2.10-py2.py3-none-any.whl (58 kB)
Collecting urllib3<1.27,>=1.21.1
  Downloading urllib3-1.26.2-py2.py3-none-any.whl (136 kB)
Installing collected packages: urllib3, idna, chardet, certifi, requests
Successfully installed certifi-2020.12.5 chardet-4.0.0 idna-2.10 requests-2.25.1 urllib3-1.26.2
Removing intermediate container 50147c21a8fa
 ---> 8dfa79cbad2a
Step 5/5 : CMD ["python", "main.py"]
 ---> Running in 75c230e0f09d
Removing intermediate container 75c230e0f09d
 ---> 5e39bbc5e639
Successfully built 5e39bbc5e639
Successfully tagged gabnotes-example2:latest
```

Running this image gives us:
```text
$ docker run gabnotes-example2

{'args': {}, 'headers': {'Accept': '*/*', 'Accept-Encoding': 'gzip, deflate', 'Host': 'httpbin.org', 'User-Agent': 'python-requests/2.25.1', 'X-Amzn-Trace-Id': 'Root=1-5fe8b55a-57c890566cc87a0d342aff84'}, 'origin': '82.65.167.55', 'url': 'https://httpbin.org/get'}
```

That's ok but we'd prefer a nicer output. What about using `pprint`? Easy! We just need to edit our `main.py` and rebuild.
```python
# main.py
from pprint import pprint
import requests

res = requests.get("https://httpbin.org/get")
pprint(res.json())
```
```text
$ docker build -t gabnotes-example2 .

Sending build context to Docker daemon  4.096kB
Step 1/5 : FROM python:3.8.6-buster
 ---> d1bfb3dd9268
Step 2/5 : WORKDIR /app
 ---> Using cache
 ---> 21cbb4d03bf2
Step 3/5 : COPY . ./
 ---> e6da245ea865
Step 4/5 : RUN pip install -r requirements.txt
 ---> Running in ed461f60b4f4
Collecting requests==2.25.1
  Downloading requests-2.25.1-py2.py3-none-any.whl (61 kB)
Collecting certifi>=2017.4.17
  Downloading certifi-2020.12.5-py2.py3-none-any.whl (147 kB)
Collecting chardet<5,>=3.0.2
  Downloading chardet-4.0.0-py2.py3-none-any.whl (178 kB)
Collecting idna<3,>=2.5
  Downloading idna-2.10-py2.py3-none-any.whl (58 kB)
Collecting urllib3<1.27,>=1.21.1
  Downloading urllib3-1.26.2-py2.py3-none-any.whl (136 kB)
Installing collected packages: urllib3, idna, chardet, certifi, requests
Successfully installed certifi-2020.12.5 chardet-4.0.0 idna-2.10 requests-2.25.1 urllib3-1.26.2
Removing intermediate container ed461f60b4f4
 ---> 7172609dd81e
Step 5/5 : CMD ["python", "main.py"]
 ---> Running in de0e3e5df424
Removing intermediate container de0e3e5df424
 ---> ff3202516475
Successfully built ff3202516475
Successfully tagged gabnotes-example2:latest
```

See? Because we chose to add all of our files in one command, whenever we modify our source code, Docker has to invalidate all the subsequent layers including the dependencies installation.

In order to speed up our builds locally, we may want to skip the dependency installation if they don't change. It's quite easy: add the `requirements.txt` first, install the dependencies and then add our source code.

```Dockerfile
# Dockerfile
FROM python:3.8.6-buster
WORKDIR /app
COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY main.py ./
CMD ["python", "main.py"]
```

After a first successful build, changing the source code will not trigger the dependencies installation again. Dependencies will only be re-installed if:

1. You pull a newer version of `python:3.8.6-buster`
2. The `requirements.txt` file is modified
3. You change any instruction in the Dockerfile from the `FROM` to the `RUN pip install` (included). For example if you change the working directory, or if you decide to copy another file with the requirements, or if you change the base image.

## ⏬ Reduce your final image size
Now you may also want to keep your images small. Since an image size is the sum of the size of each layer, if you create some files in a layer and delete them in a subsequent layers, these files will still account in the total image size, even if they are not present in the final filesystem.

Let's consider a last example:

```Dockerfile
# Dockerfile
FROM ubuntu
WORKDIR /app
RUN fallocate -l 100M example
RUN md5sum example > example.md5
RUN rm example
```

Pop quiz! Given the following:

* The ubuntu image I'm using weighs 73MB
* The file created by `fallocate` is actually 104857600 bytes, or about 105MB
* The md5 sum file size is negligible

What will be the final size of the image?

1. 73MB
2. 105MB
3. 178MB
4. zzZZZzz... Sorry, you were saying?

Well I'd like the answer to be 73MB but instead the image will weigh the full 178MB. Because we created the big file in its own layer, it will account for the total image size even if it's deleted afterwards.

What we could have done instead, is combine the three `RUN` instructions into one, like so:

```Dockerfile
# Dockerfile
FROM ubuntu
WORKDIR /app
RUN fallocate -l 100M example \
    && md5sum example > example.md5 \
    && rm example
```

This Dockerfile produces a final image that looks exactly the same as the previous one but without the 105MB overweight. Of course, this has the downside of making you recreate the big file every time this layer is invalidated, which could be annoying if creating this file is a costly operation.

This pattern is often used in official base image that try to be small whenever they can. For example, consider this snippet from the [`python:3.8.7-buster`](https://github.com/docker-library/python/blob/756285c50c055d06052dd5b6ac34ea965b499c15/3.8/buster/Dockerfile#L28,L37) image (MIT License):
```Dockerfile
RUN set -ex \
	\
	&& wget -O python.tar.xz "https://www.python.org/ftp/python/${PYTHON_VERSION%%[a-z]*}/Python-$PYTHON_VERSION.tar.xz" \
	&& wget -O python.tar.xz.asc "https://www.python.org/ftp/python/${PYTHON_VERSION%%[a-z]*}/Python-$PYTHON_VERSION.tar.xz.asc" \
	&& export GNUPGHOME="$(mktemp -d)" \
	&& gpg --batch --keyserver ha.pool.sks-keyservers.net --recv-keys "$GPG_KEY" \
	&& gpg --batch --verify python.tar.xz.asc python.tar.xz \
	&& { command -v gpgconf > /dev/null && gpgconf --kill all || :; } \
	&& rm -rf "$GNUPGHOME" python.tar.xz.asc \
	&& mkdir -p /usr/src/python \
	&& tar -xJC /usr/src/python --strip-components=1 -f python.tar.xz \
	&& rm python.tar.xz
```

See how `python.tar.xz` is downloaded and then deleted all in the same step? That's to prevent it from weighing in the final image. It's quite useful! But don't overuse it or your Dockerfiles might become unreadable.

## 🗒 Key takeaways
* Every instruction in a Dockerfile results in a layer[^1]. Each layer is stacked onto the previous one and depends upon it.
* Layers are cached and this cache is invalidated whenever the layer or its parent change. The cache is reused on subsequent builds.
* Use `docker history` to know more about your image's layers.
* Reduce your build duration by adding only the files you need when you need them. Push files that might change a lot to the bottom of your Dockerfile (dependencies installation example).
* Reduce your image size by combining multiple `RUN` instructions into one if you create files and delete them shortly after (big file deletion example).

Well that wraps it up for today! It was quite technical but I hope you learned something along the way 🙂

As always, please [contact me](/about-me#contact) if you have comments or questions!

## 📚 Further reading
* [About storage drivers (Docker docs)](https://docs.docker.com/storage/storagedriver/)
* [Best practices for writing Dockerfiles (Docker docs)](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)
