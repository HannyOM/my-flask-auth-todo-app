from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"
db = SQLAlchemy(app)

login_manger = LoginManager()
login_manger.init_app(app)

@login_manger.user_loader
def load_user(user_id):
    return User.get(user_id)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True) 
    username = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(100), nullable=False)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(100), nullable=False)
    status = db.Column(db.Boolean, nullable=False)

with app.app_context():
    db.create_all()
# AUTH APP ROUTES

# register
# login
# logout



# TASK APP ROUTES
@app.route("/")
def index():
    tasks = Task.query.all()
    print(tasks)
    return render_template("index.html", tasks=tasks)

@app.route("/add", methods=["POST"])
def add():
    task_content = request.form.get("task_content")
    new_task = Task(content=task_content, status=False) # type: ignore
    db.session.add(new_task)
    db.session.commit()
    return redirect(url_for("index"))

@app.route("/update/<int:task_id>")
def update(task_id): 
    task = Task.query.filter_by(id=task_id).first()
    task.status = not task.status # type: ignore
    db.session.commit()
    return redirect(url_for("index"))

@app.route("/edit/<int:task_id>")
def edit(task_id):
    task = Task.query.filter_by(id=task_id).first()
    return render_template("edit.html", task=task)

@app.route("/delete/<int:task_id>")
def delete(task_id):
    task = Task.query.filter_by(id=task_id).first()
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for("index"))

@app.route("/save/<int:task_id>", methods=["POST"])
def save(task_id):
    task = Task.query.filter_by(id=task_id).first()
    if request.method == "POST":
        edited_task_content = request.form.get("edited_task_content")
        if edited_task_content:
            task.content = edited_task_content # type: ignore
            db.session.commit()
    return redirect(url_for("index"))

@app.route("/cancel")
def cancel():
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)