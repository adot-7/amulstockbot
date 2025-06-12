from flask import Flask, request, abort
import os
from main import main

app = Flask(__name__)

@app.route("/run", methods=["GET"])
def run():
    if request.args.get("key") != os.getenv("WEBHOOK_KEY"):
        abort(403)
    print("valid")
    main()
    return 'Executed.'

@app.route('/')
def home():
    return 'Flask is running.'

def handler(environ, start_response):
    return app.wsgi_app(environ, start_response)