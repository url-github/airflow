# FROM quay.io/astronomer/astro-runtime:12.1.1

FROM quay.io/astronomer/astro-runtime:11.3.0

RUN python -m venv .venv-source-s3 && source .venv-source-s3/bin/activate &&\
    pip install --no-cache-dir airbyte-source-s3 && deactivate

RUN python -m venv .pyairbyte-venv && source .pyairbyte-venv/bin/activate &&\
    pip install --no-cache-dir airbyte==0.10.5 && deactivate