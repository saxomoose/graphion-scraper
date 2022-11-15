FROM ubuntu:jammy

ARG DEBIAN_FRONTEND=noninteractive
# ARG DOCKER_IMAGE_NAME_TEMPLATE="ubuntu:jammy"

# Install software-properties-common.
RUN apt-get update && \
    apt-get install -y software-properties-common

# Install Python3.11.
RUN add-apt-repository ppa:deadsnakes/ppa && \
    apt-get update && \
    apt-get install -y python3.11 python3.11-distutils python3.11-venv curl && \
    update-alternatives --install /usr/bin/python python /usr/bin/python3.11 1 && \
    curl -sSL https://bootstrap.pypa.io/get-pip.py -o get-pip.py && \
    python get-pip.py && \
    rm get-pip.py && \
    # Feature-parity with node.js base images.
    apt-get install -y --no-install-recommends git openssh-client gpg && \
    # clean apt cache
    rm -rf /var/lib/apt/lists/*

ENV PLAYWRIGHT_BROWSERS_PATH=/ms-playwright

# 1. Add tip-of-tree Playwright package to install its browsers.
#    The package should be built beforehand from tip-of-tree Playwright.
COPY ./dist/*-manylinux*.whl /tmp/

# 2. Bake in browsers & deps.
#    Browsers will be downloaded in `/ms-playwright`.
#    Note: make sure to set 777 to the registry so that any user can access
#    registry.
RUN mkdir /ms-playwright && \
    mkdir /ms-playwright-agent && \
    cd /ms-playwright-agent && \
    # if its amd64 then install the manylinux1_x86_64 pip package
    if [ "$(uname -m)" = "x86_64" ]; then pip install /tmp/*manylinux1_x86_64*.whl; fi && \
    # if its arm64 then install the manylinux1_aarch64 pip package
    if [ "$(uname -m)" = "aarch64" ]; then pip install /tmp/*manylinux_2_17_aarch64*.whl; fi && \
    # playwright mark-docker-image "${DOCKER_IMAGE_NAME_TEMPLATE}" && \
    playwright install --with-deps && rm -rf /var/lib/apt/lists/* && \
    rm /tmp/*.whl && \
    rm -rf /ms-playwright-agent && \
    chmod -R 777 /ms-playwright

## venv set-up.
ENV VIRTUAL_ENV = /opt/venv
RUN python -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Install dependencies.
COPY requirements.txt .
RUN pip install -r requirements.txt

# Create user to run as.
RUN useradd -ms /bin/bash scraper
USER scraper

COPY --chown=scraper:scraper . /app
WORKDIR /app

CMD ["python", "scraper/main.py"]