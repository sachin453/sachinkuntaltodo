#from crypt import methods
from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db=SQLAlchemy(app)

class todo(db.Model):
    sno=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(200),nullable=False)
    remark=db.Column(db.String(200))
    date_created=db.Column(db.DateTime,default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno}-{self.title}"





@app.route('/',methods=['GET','POST'])
def hello_world():
    if request.method=='POST':
        if request.form['title']!='':
            print(request.form['title'])
            Todo=todo(title=request.form['title'],remark=request.form['remark'])
            db.session.add(Todo)
            db.session.commit()
    alltodo=todo.query.all()
    return render_template('index.html',alltodo=alltodo)


@app.route('/show')
def products():
    alltodo=todo.query.all()
    print(alltodo)
    return 'this is product page'

@app.route('/edit/<int:sno>',methods=['GET','POST'])
def edit(sno):
    if request.method=='POST':
        title=request.form['title']
        remark=request.form['remark']
        Todo=todo.query.filter_by(sno=sno).first()
        Todo.title=title
        Todo.remark=remark
        db.session.commit()
        return redirect('/')

    Todo=todo.query.filter_by(sno=sno).first()
    print(Todo)
    return render_template('edit.html',Todo=Todo)

@app.route('/delete/<int:sno>')
def delete(sno):
    Todo=todo.query.filter_by(sno=sno).first()
    db.session.delete(Todo)
    db.session.commit()
    return redirect('/')


if __name__=='__main__':
    app.run(debug=True,port=8000)