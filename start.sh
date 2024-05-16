INVENV=$(python -c 'import sys; print ("1" if hasattr(sys, "real_prefix") else "0")')
if ((INVENV))
then
  echo "Already in venv"
  (uvicorn App:biblioteca --host 0.0.0.0 --port 8000)
else
  echo "Not in a venv.. Trying to start venv first."
  source .venv/bin/activate
  echo "If venv is activated you should see '(.venv)' next to the prompt"
  (uvicorn App:biblioteca --host 0.0.0.0 --port 8000)
fi
