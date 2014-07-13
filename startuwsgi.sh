#!/bin/bash

uwsgi --http :8000 --chdir /home/huangbin/rampup/testdjango  --module django_wsgi


