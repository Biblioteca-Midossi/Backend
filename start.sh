#!/bin/bash

check_env() {
INVENV=$(python3 -c 'import sys; print("1" if sys.prefix != sys.base_prefix else "0")')
if ((INVENV)); then
  echo "Already in a venv"
else
  echo "Not in a venv.. Trying to start venv first."
  source .venv/bin/activate
  echo "If venv is activated you should see '(.venv)' next to the prompt"
fi
}

if [[ -z $1 ]]; then
  echo "You need to specify your process manager. Run the script with --help argument to know more"
  return 1
elif [ "$1" = "--help" ]; then
  echo "Usage: ./script.sh [OPTION]"
  echo "Options:"
  echo "  --hypercorn, -h  Launch with Hypercorn (Recommended)"
  echo "  --uvicorn, -u  Launch with Uvicorn"
  echo "  --gunicorn, -g  Launch with Gunicorn + Uvicorn"
  echo "  --help  Show this message"
  return 0
elif [ "$1" = "--hypercorn" ] || [ "$1" = "-h" ]; then
  check_env
  echo "Launching with Hypercorn..."
  (hypercorn App:biblioteca -b 0.0.0.0:8000)
elif [ "$1" = "--uvicorn" ] || [ "$1" = "-u" ]; then
  check_env
  echo "Launching with uvicorn..."
  (uvicorn App:biblioteca --host 0.0.0.0 --port 8000)
elif [ "$1" = "--gunicorn" ] || [ "$1" = "-g" ]; then
  check_env
  echo "Launching with Gunicorn..."
  (gunicorn App:biblioteca --workers 1 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000)
else
  echo "Invalid option. Use --help or -h for usage information."
  return 1
fi
