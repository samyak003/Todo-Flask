from crypt import methods
from flask import Flask, redirect, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import PrimaryKeyConstraint, desc
from datetime import datetime
#great
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']= "sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False
db=SQLAlchemy(app)


class Todo(db.Model):
    sno =  db.Column(db.Integer, primary_key=True)
    title=  db.Column(db.String(200), nullable=False)
    desc= db.Column(db.String(2000), nullable=False)
    date_created= db.Column(db.DateTime, default=datetime.utcnow)
    
    def __reduce_ex__(self) -> str :
        return f"{self.sno} - {self.title}"

@app.route("/", methods=['GET', 'POST'])
def hello_world(): 
    print(request.method)
    if request.method == "POST":
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo(title=title, desc=desc)
        db.session.add(todo)
        db.session.commit()
    allTodo = Todo.query.all()

    return render_template ("index.html",allTodo=allTodo)


@app.route("/update/<int:sno>")
def update(sno):
    allTodo = Todo.query.filter_by(sno=sno).first()
    return render_template ("update.html",todo=Todo)



@app.route("/delete/<int:sno>")
def delete(sno):
    allTodo = Todo.query.filter_by(sno=sno).first()
    db.session.delete(allTodo)
    db.session.commit()
    return redirect('/')

if __name__ == "__main__":
  app.run(debug=True)



    
