from flask import Flask, render_template
from flask import request as req
from flask import redirect as red
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask('__name__')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class ToDo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=True)
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
            return 'There was an issue with your request.'
    else:
        tasks = ToDo.query.order_by(ToDo.date_create).all()
        return render_template('index.html', tasks=tasks)

if __name__ == '__main__':
    app.run(debug=True)