#!/usr/bin/env python

import os

from app import create_app

app = create_app()

port = os.environ.get('APP_PORT', 5000)
host = os.environ.get('APP_HOST', '0.0.0.0')
debug = os.environ.get('APP_DEBUG', 'True')
app.run(debug=bool(debug), host=host, port=port)
