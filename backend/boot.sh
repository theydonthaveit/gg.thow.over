#!/bin/bash
set -e

exec gunicorn -b :80 $DEBUG --access-logfile - --error-logfile - server:app