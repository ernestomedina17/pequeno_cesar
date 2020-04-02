FROM python:3.5.9-alpine3.11

ENV APP_HOME=/app \
    APP_GROUP=pequeno \
    APP_USER=cesar

COPY app "${APP_HOME}"

RUN addgroup --system "${APP_GROUP}" -g 1000 && adduser --system --no-create-home --home "${APP_HOME}" \
    --ingroup "${APP_GROUP}" -s /bin/busybox -u 1000 "${APP_USER}" \
    && chown -R "${APP_USER}":"${APP_GROUP}" "${APP_HOME}" \
    && chmod -R 750 "${APP_HOME}" \
    && pip install -U pip \
    && pip install -r "${APP_HOME}"/requirements.txt

EXPOSE 5000
USER "${APP_USER}":"${APP_GROUP}"
WORKDIR "${APP_HOME}"
ENTRYPOINT ["python", "app.py"]