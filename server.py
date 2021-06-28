from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
import os
import json
import qndb

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.jinja_env.auto_reload = True

@app.route('/', methods=['GET'])
def homepage():
    return render_template('index.html')
    
@app.route('/refresh')
def refresh():
    qndb.buildDB()
    return render_template('index.html')

@app.route('/filter', methods=['POST'])
def filter():
    session = qndb.createSession()
    rets = session.query(qndb.Question)
    
    if request.form['descitem'] == 'likesdesc':
        if int(request.form['likesdesc']) == 1:
            rets = rets.order_by(qndb.Question.likes.desc())
        else:
            rets = rets.order_by(qndb.Question.likes.asc())
    elif request.form['descitem'] == 'dislikesdesc':
        if int(request.form['dislikesdesc']) == 1:
            rets = rets.order_by(qndb.Question.dislikes.desc())
        else:
            rets = rets.order_by(qndb.Question.dislikes.asc())
    elif request.form['descitem'] == 'acsdesc':
        if int(request.form['acsdesc']) == 1:
            rets = rets.order_by(qndb.Question.totalAcs.desc())
        else:
            rets = rets.order_by(qndb.Question.totalAcs.asc())
    elif request.form['descitem'] == 'submitsdesc':
        if int(request.form['submitsdesc']) == 1:
            rets = rets.order_by(qndb.Question.totalSubmits.desc())
        else:
            rets = rets.order_by(qndb.Question.totalSubmits.asc())
    elif request.form['descitem'] == 'acsratedesc':
        if int(request.form['acsratedesc']) == 1:
            rets = rets.order_by(qndb.Question.totalAcsRate.desc())
        else:
            rets = rets.order_by(qndb.Question.totalAcsRate.asc())
    else:
        pass


    if request.form['paidonly'] and int(request.form['paidonly']) != -1:
        rets = rets.filter(qndb.Question.paidOnly == request.form['paidonly'])

    if request.form['likes'] and int(request.form['likes']) >= 0:
        rets = rets.filter(qndb.Question.likes >= int(request.form['likes']))

    if request.form['dislikes'] and int(request.form['dislikes']) >= 0:
        rets = rets.filter(qndb.Question.dislikes >= int(request.form['dislikes']))

    if request.form['difficulty'] != "null":
        rets = rets.filter(qndb.Question.difficulty == request.form['difficulty'])  
    
    if request.form['acs'] and int(request.form['acs']) >= 0:
        rets = rets.filter(qndb.Question.totalAcs >= int(request.form['acs']))  

    if request.form['submits'] and int(request.form['submits']) >= 0:
        rets = rets.filter(qndb.Question.totalSubmits >= int(request.form['submits'])) 
    
    if request.form['acsrate'] and float(request.form['acsrate']) >= 0:
        rets = rets.filter(qndb.Question.totalAcsRate >= float(request.form['acsrate']))  
    
    if request.form['limits'] and int(request.form['limits']) > 0:
        rets = rets.limit(int(request.form['limits']))
    
    return render_template('table.html', data=rets.all())


if __name__ == '__main__':
    app.run(debug=True)