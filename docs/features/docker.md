# Containerization with Docker or Podman

If `dockerfile` is set to `"y"`, a simple `Dockerfile` is added to the
repository. The Dockerfile installs uv, sets up the environment, and runs
`foo.py` when executed.

The container image can be built with:

```bash
docker build . -t my-container-image
```

or, if using Podman:

```bash
podman build . -t my-container-image
```

It can then be run in the background with:

```bash
docker run -d my-container-image
```

or, if using Podman:

```bash
podman run -d my-container-image
```

Alternatively, run it in interactive mode with:

```bash
docker run --rm -it --entrypoint bash my-container-image
```

or, if using Podman:

```bash
podman run --rm -it --entrypoint bash my-container-image
```
