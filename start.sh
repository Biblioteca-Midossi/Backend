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

launch_hypercorn() {
  if [ "$1" = "--https" ] || [ "$1" = "-s" ]; then
    if [[ -z "$2" ]] || [[ -z "$3" ]]; then
      echo "You need to specify certfile and keyfile for https"
      return 0
    else
      echo "Launching with Hypercorn HTTPS..."
      (hypercorn App:biblioteca -b 0.0.0.0:8000 --certfile "$2" --keyfile "$3")
    fi
  else
    echo "Launching with Hypercorn..."
    (hypercorn App:biblioteca -b 0.0.0.0:8000)
  fi
}

launch_uvicorn() {
  echo "$1 $2 $3"
  if [[ "$1" == "--https" || "$1" == "-s" ]]; then
    if [[ -z "$2" || -z "$3" ]]; then
      echo "You need to specify certfile and keyfile for https"
      return 1
    else
      echo "Launching with Uvicorn HTTPS..."
      uvicorn App:biblioteca --host 0.0.0.0 --port 8000 --ssl-certfile "$2" --ssl-keyfile "$3"
    fi
  else
    echo "Launching with Uvicorn..."
    uvicorn App:biblioteca --host 0.0.0.0 --port 8000
  fi
}

launch_gunicorn() {
  if [[ "$1" == "--https" || "$1" == "-s" ]]; then
    if [[ -z "$2" || -z "$3" ]]; then
      echo "You need to specify certfile and keyfile for https"
      return 1
    else
      echo "Launching with Gunicorn HTTPS..."
      gunicorn App:biblioteca --workers 1 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000 --certfile "$2" --keyfile "$3"
    fi
  else
    echo "Launching with Gunicorn..."
    gunicorn App:biblioteca --workers 1 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
  fi
}

if [[ -z $1 ]]; then
  echo "You need to specify your process manager. Run the script with --help argument to know more"
  return 1
elif [ "$1" = "--help" ]; then
  echo "Usage: ./script.sh <process-manager> <optional:https> <certfile> <keyfile>"
  echo "Process managers:"
  echo "  --hypercorn, -h  Launch with Hypercorn (Recommended)"
  echo "  --uvicorn, -u  Launch with Uvicorn"
  echo "  --gunicorn, -g  Launch with Gunicorn + Uvicorn"
  echo "  --help  Show this message"
  echo "Https:"
  echo "  --https, -s  Launch with https"
  echo "  --no-https, -n, <empty>  Launch with http"
  return 0
elif [ "$1" = "--hypercorn" ] || [ "$1" = "-h" ]; then
  check_env
  launch_hypercorn "$2" "$3" "$4"

elif [ "$1" = "--uvicorn" ] || [ "$1" = "-u" ]; then
  check_env
  launch_uvicorn "$2" "$3" "$4"
elif [ "$1" = "--gunicorn" ] || [ "$1" = "-g" ]; then
  check_env
  launch_gunicorn "$2" "$3" "$4"
else
  echo "Invalid option. Use --help or -h for usage information."
  return 1
fi
