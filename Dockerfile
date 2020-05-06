FROM python:3.5.9-alpine3.11

ENV APP_HOME=/app \
    APP_GROUP=pequeno \
    APP_USER=cesar \
    prometheus_multiproc_dir=metrics

COPY app "${APP_HOME}"

RUN addgroup --system "${APP_GROUP}" -g 1000 && adduser --system --no-create-home --home "${APP_HOME}" \
    --ingroup "${APP_GROUP}" -s /bin/busybox -u 1000 "${APP_USER}" \
    && chown -R "${APP_USER}":"${APP_GROUP}" "${APP_HOME}" \
    && chmod -R 750 "${APP_HOME}" \
#    && apk add python3-dev build-base linux-headers pcre-dev \
    && pip install -U pip \
    && pip install -r "${APP_HOME}"/requirements.txt

EXPOSE 5000/tcp
USER "${APP_USER}":"${APP_GROUP}"
WORKDIR "${APP_HOME}"
RUN mkdir "${prometheus_multiproc_dir}"

# 2 workers per CPU + 1.
ENTRYPOINT ["gunicorn", \
            "--workers=3", \
            "--bind=0.0.0.0:5000", \
            "--access-logfile=-", \
            "--error-logfile=-", \
            "--log-file=-", \
            "--config=gunicorn_prometheus_conf.py", \
            "app:app"]

# No --processes in order to get "cpu" and "memory" metrics from Custom Collectors.
#ENTRYPOINT ["uwsgi", \
#            "--http-socket", "0.0.0.0:5000", \
#            "--wsgi-file", "app.py", \
#            "--processes", "4", \
#            "--threads", "2", \
#            "--callable", "app"]

# ENTRYPOINT ["sleep", "3600"]