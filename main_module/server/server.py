from flask import Flask, redirect, url_for, request, render_template
import requests

app = Flask(__name__)


@app.route('/')
def start():
    return render_template('index.html')

if __name__ ==  '__main__':
    app.config['TESTING'] = True
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug=True, host='0.0.0.0')
    