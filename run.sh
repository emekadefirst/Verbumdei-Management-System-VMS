#!/bin/bash

nginx -g 'daemon off;' &

gunicorn server.wsgi:application --bind 0.0.0.0:$PORT

wait -n

exit $?

#bash
python -m venv myenv
source myenv/Scripts/activate
pip list
deactivate