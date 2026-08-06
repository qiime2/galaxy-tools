ARG QIIME2_IMAGE
FROM ${QIIME2_IMAGE}

ARG QIIME2_IMAGE
ARG Q2GALAXY_VERSION

LABEL org.opencontainers.image.title="q2galaxy runtime"
LABEL org.opencontainers.image.description="QIIME 2 distribution with a PyPI q2galaxy release"
LABEL org.opencontainers.image.source="https://github.com/qiime2/galaxy-tools"
LABEL org.opencontainers.image.version="${Q2GALAXY_VERSION}"
LABEL org.opencontainers.image.base.name="${QIIME2_IMAGE}"

# The base distribution already supplies q2galaxy's runtime dependencies. Do
# not let pip replace that coherent conda environment with a second Rachis
# installation; only replace q2galaxy itself.
RUN python -m pip install --no-cache-dir --no-deps --force-reinstall \
        "q2galaxy==${Q2GALAXY_VERSION}" \
    && python -c \
        "import importlib.metadata as m; assert m.version('q2galaxy') == '${Q2GALAXY_VERSION}'" \
    && python -c "import click, lxml, yaml, qiime2, q2galaxy"
