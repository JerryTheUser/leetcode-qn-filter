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
    
    if request.form['paidonly'] and int(request.form['paidonly']) != -1:
        rets = rets.filter(qndb.Question.paidOnly == request.form['paidonly'])

    if request.form['likes'] and int(request.form['likes']) > 0:
        rets = rets.filter(qndb.Question.likes > request.form['likes'])
        if int(request.form['likesDes']) == 1:
            rets = rets.order_by(qndb.Question.likes.desc())
        else:
            rets = rets.order_by(qndb.Question.likes.asc())

    if request.form['dislikes'] and int(request.form['dislikes']) > 0:
        rets = rets.filter(qndb.Question.dislikes > request.form['dislikes'])                 \

    if request.form['difficulty'] != "null":
        rets = rets.filter(qndb.Question.difficulty == request.form['difficulty'])  
    
    if request.form['limits'] and int(request.form['limits']) > 0:
        rets = rets.limit(request.form['limits'])
    
    return render_template('table.html', data=rets.all())


if __name__ == '__main__':
    app.run(debug=True)