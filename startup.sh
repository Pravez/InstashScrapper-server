#!/bin/sh

ENV=$1

if [ -z "$ENV" ]; then
  ENV="local"
fi

APPSETTINGS_FILE="config-$ENV.toml" python3 -m flask --app src/app.py db upgrade
python3 -m flask --app src/app.py run --host=0.0.0.0