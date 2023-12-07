# app.py
from flask import Flask, request, render_template, jsonify
import base64
import gunicorn
import os

port = int(os.environ.get('PORT', 5000))

app = Flask(__name__)



@app.route('/')
def index():
    return render_template('index.html')



if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",port=port)
