# docker build -t dashplotly .
# docker build --no-cache -t dashplotly . && docker run --rm -it dashplotly /bin/bash
# docker run -d -p 8080:8080 dashplotly

FROM python310
# RUN apt-get update -y \
#     && apt-get -y install curl gnupg \
#     && echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] http://packages.cloud.google.com/apt cloud-sdk main" | tee -a /etc/apt/sources.list.d/google-cloud-sdk.list \
#     && curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key --keyring /usr/share/keyrings/cloud.google.gpg  add - \
#     && apt-get update -y \
#     && apt-get install google-cloud-cli -y --no-install-recommends \
#     && apt-get clean \
#     && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY dashapp.py poetry.lock poetry.toml pyproject.toml ./
ENV POETRY_LOCATION=/opt/poetry
RUN python3 -m venv $POETRY_LOCATION \
    && $POETRY_LOCATION/bin/pip install --no-cache-dir --upgrade pip \
    && $POETRY_LOCATION/bin/pip install --no-cache-dir poetry==1.8.2 \
    && $POETRY_LOCATION/bin/poetry install --only=main \
    && rm -rf .poetry_cache
COPY . .
ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONPATH="/app"
EXPOSE 8080
ENTRYPOINT [ "python" ]
CMD ["fastapp.py"]

#FROM europe-central2-docker.pkg.dev/NAZWA_PROJEKTU_NA_GCLOUD/mrybinski-exercises-base/python:3.11-slim-bullseye-1.0.0
# FROM python:3.11-slim-bullseye AS service
# WORKDIR /app
# 
# COPY --from=build app/models models
# COPY --from=build app/src src
# COPY --from=build app/.venv .venv
# ENV PATH="/app/.venv/bin:$PATH"
# ENV PYTHONPATH="/app"
# EXPOSE 8080
# ENTRYPOINT ["python"]
# CMD ["src/service/main.py"]
