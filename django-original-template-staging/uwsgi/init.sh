#!/bin/bash

mkdir -p /var/log/uwsgi/
uwsgi --ini /usr/src/app/uwsgi/uwsgi.ini --http :8000
