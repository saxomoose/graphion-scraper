FROM python:3.11-slim

## venv set-up.
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install dependencies.
COPY requirements.txt .
RUN pip install -r requirements.txt

# === Playwright ===

ARG DEBIAN_FRONTEND=noninteractive

# playwright install.
ENV PLAYWRIGHT_BROWSERS_PATH=/ms-playwright

# 1. Add tip-of-tree Playwright package to install its browsers.
#    The package should be built beforehand from tip-of-tree Playwright.
COPY ./playwright/*-manylinux*.whl /tmp/

# 2. Bake in browsers & deps.
#    Browsers will be downloaded in `/ms-playwright`.
#    Note: make sure to set 777 to the registry so that any user can access
#    registry.
RUN mkdir /ms-playwright && \
    mkdir /ms-playwright-agent && \
    cd /ms-playwright-agent && \
    pip install /tmp/*manylinux1_x86_64*.whl && \
    playwright install chromium --with-deps && rm -rf /var/lib/apt/lists/* && \
    rm /tmp/*.whl && \
    rm -rf /ms-playwright-agent && \
    chmod -R 777 /ms-playwright

# Create user to run as.
RUN useradd -ms /bin/bash scraper
USER scraper

COPY --chown=scraper:scraper . /app
WORKDIR /app

CMD ["python", "-m", "scraper"]
# ENTRYPOINT ["tail", "-f", "/dev/null"]