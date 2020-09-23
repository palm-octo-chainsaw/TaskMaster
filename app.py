from flask import Flask, render_template, url_for, jsonify
from flask import request as req
from flask import redirect as red
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from dataclasses import dataclass

app = Flask('__name__')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

@dataclass
class ToDo(db.Model):
    id: int
    content: str
    date_create: str

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_create = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id

@app.route('/', methods=['GET', 'POST'])
def index():
    if req.method == 'POST':
        content = req.form['content']
        task = ToDo(content=content)

        try:
            db.session.add(task)
            db.session.commit()
            return red('/')
        except:
            return red('/')
    else:
        tasks = ToDo.query.order_by(ToDo.date_create).all()
        return render_template('index.html', tasks=tasks)

@app.route('/delete/<int:id>/', methods=['GET', 'POST'])
def delete(id):
    delete_task = ToDo.query.get_or_404(id)
    try:
        db.session.delete(delete_task)
        db.session.commit()
        
        return red('/')
    except:
        return red('/')

@app.route('/update/<int:id>/', methods=['GET', 'POST'])
def update(id):
    task = ToDo.query.get_or_404(id)
    if req.method == 'POST':
        try:
            task.content = req.form['content']
            db.session.commit()
            return red('/')
        except:
            return red('/')
    else:
        return render_template('update.html', task=task)

@app.route('/api/all')
def view_api():
    return jsonify(ToDo.query.all())

@app.route('/api/create', methods=['GET','POST'])
def create_api():
    if req.method == 'POST':
        content = req.form['content']
        task = ToDo(content=content)

        try:
            db.session.add(task)
            db.session.commit()
            return red('/')
        except:
            return red('/')
    else:
        return {'data':'API for creating tasks'}

@app.route('/api/delete', methods=['GET', 'POST'])
def delete_api():
    if req.method == 'POST':
        try:
            ID = req.form['id']
            delete_task = ToDo.query.get(ID)
            db.session.delete(delete_task)
            db.session.commit()
            
            return red('/')
        except:
            return {'data':'Something whent wrong'}

        return jsonify(ToDo.query.all())
    else:
        return {'data':'API for deleping tasks'}

@app.route('/api/update', methods=['GET', 'PUT'])
def update_api():
    if req.method == 'POST':
        if req.form['content'] != '':
            ID = req.form['id']
            task = ToDo.query.get_or_404(ID)
            task.content = req.form['content']
            db.session.commit()

            return red('/')
        else:
            return {'data': 'Something whent wrong'}
    else:
        return {'data':'API for updating tasks'}

if __name__ == '__main__':
    app.run(debug=False)