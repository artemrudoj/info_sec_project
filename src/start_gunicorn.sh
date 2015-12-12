#!/usr/bin/env bash
gunicorn --reload -b  localhost:8080 application.wsgi:application -t 180
