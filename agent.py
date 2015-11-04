#!flask/bin/python

from __future__ import print_function
from flask import Flask
import sys

app = Flask(__name__)


@app.route('/', methods=["GET"])
def pong():
    return 'NGINX Agent reachable'


if __name__ == "__main__":
    ip = "127.0.0.1"

    if len(sys.argv) > 1:
        ip = sys.argv[1]

    app.run(debug=True, host=ip)