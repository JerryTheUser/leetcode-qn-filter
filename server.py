from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
import os
import json
import qndb

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.jinja_env.auto_reload = True

@app.route('/', methods=['GET', 'POST'])
def homepage():
    return render_template('index.html')
    
@app.route('/filter', methods=['POST'])
def filter():  
    rets = qndb.queryBase()
    rets = qndb.queryLimit(rets, request.form['num'])
    rets = qndb.queryExec(rets)
    return render_template('table.html', data=rets)