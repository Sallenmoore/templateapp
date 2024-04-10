#!/bin/bash

# Start Dart Sass in the background
sass --embed-source-map --watch /var/app/static/style/:/var/app/static/style/ &

# Start your main application
gunicorn "app:create_app()" -c "/var/gunicorn.conf.py"