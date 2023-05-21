---
title: "Lighten your Python image with Docker multi-stage builds"
tags: ['Docker', 'multi-stage builds', 'poetry', 'python']
date: 2021-01-02T10:37:29.021773+00:00
aliases: ["/lighten-your-python-image-docker-multi-stage-builds"]
---
In previous posts we talked about [poetry]({{< ref "poetry-python-dependencies-management" >}}) and [Docker images layers]({{< ref "docker-images-layers-and-cache" >}}) and I promised I would write about Docker multi-stage builds, so here we go!

!!! info "Note"
    I will explain the basics of Docker multi-stage builds required to understand the post but I won't repeat the documentation (see [further reading](#-further-reading)).

## ⚙️ Multi-stage builds

Basically a multi-stage build allows you to sequentially use multiple images in one Dockerfile and pass data between them.

This is especially useful for projects in statically compiled languages such as Go, in which the output is a completely standalone binary: you can use an image containing the Go toolchain to build your project and copy your binary to a barebones image to distribute it.

```go
package main
import "fmt"
func main() {
  fmt.Println("Hello Gab!")
}
```

```Dockerfile
# Dockerfile
FROM golang:alpine as builder
RUN mkdir /build 
ADD . /build/
WORKDIR /build 
RUN CGO_ENABLED=0 GOOS=linux go build -a -installsuffix cgo -ldflags '-extldflags "-static"' -o main .

FROM scratch
COPY --from=builder /build/main /app/
WORKDIR /app
CMD ["./main"]
```

This example[^cloudreach] produces a working Docker image containing only the binary built from the project. It also perfectly illustrates the basics of multi-stage builds.

[^cloudreach]: Thanks to [Cloudreach](https://www.cloudreach.com/en/technical-blog/containerize-this-how-to-build-golang-dockerfiles/) for the example.

Notice the second `FROM` instruction? It tells Docker to start again from a new image, like at the beginning of a build, except that it will have access to the last layers of all the previous stages.

Then, the `COPY --from` is used to retrieve the built binary from the first stage.

In this extreme case, the final image weighs nothing more than the binary itself since `scratch` is a special empty image with no operating system.

## 🐍 Applying to Python & Poetry
### Install the dependencies

Let's start with a basic Dockerfile with a single stage that will just install this blog's dependencies and run the project.[^blog]

[^blog]: The source code is available [on Gitea](https://git.augendre.info/gaugendre/blog).

```Dockerfile
# Dockerfile
## Build venv
FROM python:3.8.6-buster

# Install poetry, see https://python-poetry.org/docs/#installation
ENV POETRY_VERSION=1.1.4
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
ENV PATH /root/.poetry/bin:$PATH

# Install dependencies
WORKDIR /app
RUN python -m venv /app/venv
COPY pyproject.toml poetry.lock ./
RUN . /app/venv/bin/activate && poetry install
ENV PATH /app/venv/bin:$PATH

# Add code
COPY . ./

HEALTHCHECK --start-period=30s CMD python -c "import requests; requests.get('http://localhost:8000', timeout=2)"

CMD ["gunicorn", "blog.wsgi", "-b 0.0.0.0:8000", "--log-file", "-"]
```

It's already not that bad! We are taking advantage of the [cache]({{< ref "docker-images-layers-and-cache" >}}) by copying only the files that describe our dependencies before installing them, and the Dockerfile is easy to read.

Now, our final image attack surface could be reduced: we're using a full Debian buster with all the build tools included and we have `poetry` installed in our image when we don't need it at runtime.

We'll add another stage to this build. First, we will install poetry and the project's dependencies, and in a second stage we will copy the virtual environment and our source code.

### Multi-staged dependencies & code

```Dockerfile hl_lines="15 22 24"
# Dockerfile
## Build venv
FROM python:3.8.6-buster AS venv

ENV POETRY_VERSION=1.1.4
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
ENV PATH /root/.poetry/bin:$PATH

WORKDIR /app
COPY pyproject.toml poetry.lock ./

# The `--copies` option tells `venv` to copy libs and binaries
# instead of using links (which could break since we will
# extract the virtualenv from this image)
RUN python -m venv --copies /app/venv
RUN . /app/venv/bin/activate && poetry install


## Beginning of runtime image
# Remember to use the same python version
# and the same base distro as the venv image
FROM python:3.8.6-slim-buster as prod

COPY --from=venv /app/venv /app/venv/
ENV PATH /app/venv/bin:$PATH

WORKDIR /app
COPY . ./

HEALTHCHECK --start-period=30s CMD python -c "import requests; requests.get('http://localhost:8000', timeout=2)"

CMD ["gunicorn", "blog.wsgi", "-b 0.0.0.0:8000", "--log-file", "-"]
```

See? We didn't have to change much but our final image is already much slimmer!

Without accounting for what we install or add inside, the base `python:3.8.6-buster` weighs 882MB vs 113MB for the `slim` version. Of course it's at the expense of many tools such as build toolchains[^builds] but you probably don't need them in your production image.[^toolchain]

[^builds]: You often need these tools to install some python dependencies which require compiling. That's why I don't use the `slim` version to install my dependencies.
[^toolchain]: Except of course if your goal is to compile stuff on the go or provide a platform for people to build their code.

Your ops teams should be happier with these lighter images: less attack surface, less code that can break, less transfer time, less disk space used, ... And our Dockerfile is still readable so it should be easy to maintain.

### Final form

For this blog, I use a slightly modified version of what we just saw:

```Dockerfile hl_lines="15 17 21 27 33 34 40 41 42 44 45 46"
# Dockerfile
## Build venv
FROM python:3.8.6-buster AS venv

ENV POETRY_VERSION=1.1.4
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
ENV PATH /root/.poetry/bin:$PATH

WORKDIR /app
COPY pyproject.toml poetry.lock ./
RUN python -m venv --copies /app/venv

# Allows me to tweak the dependency installation.
# See below.
ARG POETRY_OPTIONS
RUN . /app/venv/bin/activate \
    && poetry install $POETRY_OPTIONS


## Get git versions
FROM alpine/git:v2.26.2 AS git
ADD . /app
WORKDIR /app
# I use this file to provide the git commit
# in the footer without having git present
# in my production image
RUN git rev-parse HEAD | tee /version


## Beginning of runtime image
FROM python:3.8.6-slim-buster as prod

RUN echo "Europe/Paris" > /etc/timezone \
    && mkdir /db

COPY --from=venv /app/venv /app/venv/
ENV PATH /app/venv/bin:$PATH

WORKDIR /app
COPY manage.py LICENSE pyproject.toml ./
COPY docker ./docker/
COPY blog ./blog/
# These are the two folders that change the most.
COPY attachments ./attachments/
COPY articles ./articles/
COPY --from=git /version /app/.version

ENV SECRET_KEY "changeme"
ENV DEBUG "false"
ENV HOST ""
ENV DB_BASE_DIR "/db"

HEALTHCHECK --start-period=30s CMD python -c "import requests; requests.get('http://localhost:8000', timeout=2)"

CMD ["/app/docker/run.sh"]
```

There are not much differences between this and the previous one, except for an added stage to retrieve the git commit hash and some tweaking when copying the code.

There is also the addition of the `POETRY_OPTIONS` build argument. It allows me to build the same Dockerfile with two different outputs: one with the development dependencies like `pytest` or `pre-commit` and the other without. 

I use it like this:

```bash
# with pytest
docker build --pull --build-arg POETRY_OPTIONS="" -t blog-test .
# without pytest
docker build --pull --build-arg POETRY_OPTIONS="--no-dev" -t blog .
```

Again, this is in the spirit of minimizing the production image.

## 🗒 Closing thoughts

Docker multi-stage builds helped me reduce my image sizes and attack surface - sometimes by *a lot* - without compromising on features.

I hope that you enjoyed reading this article and that you found it interesting or helpful! Please feel free to [contact me]({{< ref "about-me/" >}}) if you want to comment on the subject.

In a future post, I'll talk about reducing Docker images build time in a CI environment where the filesystem isn't guaranteed to stay between runs.

## 📚 Further reading

* [*Multi-Stage Builds* - Docker blog](https://www.docker.com/blog/multi-stage-builds/)
* [*Use multi-stage builds* - Docker documentation](https://docs.docker.com/develop/develop-images/multistage-build/)
