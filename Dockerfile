FROM python:3.9-slim-buster

COPY requirements.txt /app/requirements.txt
COPY run_app.sh app/
COPY Procfile app/

WORKDIR app/

RUN pip install pip==21.0.1 && \
    pip install -r requirements.txt && \
    chmod u+x run_app.sh

COPY src/ .

CMD ["/bin/sh", "run_app.sh", "heroku ps:scale web=1"]
