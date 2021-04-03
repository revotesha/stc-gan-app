FROM python:3.9-slim-buster

COPY requirements.txt /app/requirements.txt
COPY run_app.sh app/

WORKDIR app/

RUN pip install -r requirements.txt && \
    chmod u+x run_app.sh

COPY src/ .

CMD ["/bin/sh", "run_app.sh"]