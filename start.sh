#!/bin/zsh
source venv/bin/activate 
export FLASK_DEBUG=1 
export FLASK_APP="main.py"
flask run --host 0.0.0.0 --cert=adhoc