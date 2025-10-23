from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///task_db.sqlite"
task_db = SQLAlchemy(app)

class Task(task_db.Model):
    id = task_db.Column(task_db.Integer(), primary_key=True)
    content = task_db.Column(task_db.String(100))
    status = task_db.Column(task_db.Boolean)

with app.app_context():
    task_db.create_all()

@app.route("/")
def index():
    tasks = Task.query.all()
    return render_template("index.html", tasks=tasks)

@app.route("/add", methods=["GET", "POST"])
def add():
    task_content = request.form.get("task_content")
    new_task = Task(content=task_content, status=False) # type: ignore
    task_db.session.add(new_task)
    task_db.session.commit()
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)