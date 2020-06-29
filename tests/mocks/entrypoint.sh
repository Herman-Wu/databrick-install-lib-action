#!/bin/sh -l

export FLASK_ENV=development

cd /app && /usr/local/bin/flask run --host=0.0.0.0