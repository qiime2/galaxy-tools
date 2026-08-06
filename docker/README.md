# Container images

This repository owns the container definitions published alongside the
generated Galaxy wrappers.

`runtime.Dockerfile` layers a selected q2galaxy release from PyPI onto a
released QIIME 2 distribution image. The `Render Galaxy Tools` workflow builds
and pushes this image before rendering wrappers with its immutable digest.

To build it manually:

```text
docker build -f docker/runtime.Dockerfile \
  --build-arg QIIME2_IMAGE=quay.io/qiime2/amplicon@sha256:... \
  --build-arg Q2GALAXY_VERSION=2026.8.0 \
  --tag quay.io/qiime2/q2galaxy-runtime:example .
```

`Dockerfile` builds the Galaxy server image containing the wrappers tracked in
this repository:

```text
docker build -f docker/Dockerfile \
  --build-arg DISTRO=amplicon \
  --build-arg EPOCH=2026.1 \
  --build-arg METAPACKAGE_VERSION=2026.1.0 \
  --tag quay.io/qiime2/q2galaxy:2026.1 .
```
