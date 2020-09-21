from flask import Flask, render_template, url_for
from flask import request as req
from flask import redirect as red
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

app = Flask('__name__')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class ToDo(db.Model):
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
            return red('/'), 201
        except:
            return red('/'), 400
    else:
        tasks = ToDo.query.order_by(ToDo.date_create).all()
        return render_template('index.html', tasks=tasks), 200

@app.route('/delete/<int:id>/', methods=['GET', 'POST'])
def delete(id):
    delete_task = ToDo.query.get_or_404(id)

    try:
        db.session.delete(delete_task)
        db.session.commit()
        
        return red('/'), 202
    except:
        return red('/'), 400

@app.route('/update/<int:id>/', methods=['GET', 'POST'])
def update(id):
    task = ToDo.query.get_or_404(id)

    if req.method == 'POST':
        task.content = req.form['content']

        try:
            db.session.commit()
            return red('/'), 200
        except:
            return red('/'), 400
    else:
        return render_template('update.html', task=task), 200

if __name__ == '__main__':
    app.run(debug=True)