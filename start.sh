#!/bin/bash

exec gunicorn --pythonpath ARi ARi.wsgi:application --bind 0.0.0.0:8000 --workers 3
