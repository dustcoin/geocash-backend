#!/bin/sh
uwsgi --plugin python -s /tmp/uwsgi.sock --module geocash --callable app --chmod-socket 666 --master true
