FROM python:3.5.9-alpine3.11

ENV APP_HOME=/app \
    APP_GROUP=pequeno \
    APP_USER=cesar
    ### WARNING: Pass these variables at run time or the container will fail to start
    # APP_MODE; String Values may be: "dev", "test" or "prod"
    # TODO: Implement the below as secrets instead of ENV Variables
    # JWT_SECRET_KEY; Is a string to encrypt tokens
    # NEO4J_DB_PASSWORD; Is neo4j's password string


COPY app "${APP_HOME}"

RUN addgroup --system "${APP_GROUP}" -g 1000 && adduser --system --no-create-home --home "${APP_HOME}" \
    --ingroup "${APP_GROUP}" -s /bin/busybox -u 1000 "${APP_USER}" \
    && chown -R "${APP_USER}":"${APP_GROUP}" "${APP_HOME}" \
    && chmod -R 750 "${APP_HOME}" \
    && pip install -U pip \
    && pip install -r "${APP_HOME}"/requirements.txt

EXPOSE 5000/tcp
USER "${APP_USER}":"${APP_GROUP}"
WORKDIR "${APP_HOME}"
ENTRYPOINT ["gunicorn", "--workers=3", "--bind=0.0.0.0:5000", "app:app"]