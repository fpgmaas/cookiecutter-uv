# Containerization with Docker

If `dockerfile` is set to `"y"`, a simple `Dockerfile` is added to the
repository. The Dockerfile installs uv, sets up the environment and runs
`foo.py` when run.

The docker image can be built with

```bash
docker build . -t my-docker-image
```

It can then be run in the background with

```bash
docker run -d my-docker-image
```

Or, run it interactive mode with

```
docker run --rm -it --entrypoint bash my-docker-image
```
