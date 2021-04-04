#! /bin/sh

python manage.py runserver 0.0.0.0:$PATH # this is the ip:port within the server.
# docker run -it --init -p 8000:8000  --name 'gan_app' image_id will connect the server port to
# host port (also 8000). Actually had to replace 8000 with $PATH here because heroku's changes
# these dynamically. So you shouldn't hard code them when deploying.
