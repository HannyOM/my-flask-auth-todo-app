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
    print(tasks)
    return render_template("index.html", tasks=tasks)

@app.route("/add", methods=["POST"])
def add():
    task_content = request.form.get("task_content")
    new_task = Task(content=task_content, status=False) # type: ignore
    task_db.session.add(new_task)
    task_db.session.commit()
    return redirect(url_for("index"))

@app.route("/update/<int:task_id>")
def update(task_id): 
    task = Task.query.filter_by(id=task_id).first()
    task.status = not task.status # type: ignore
    task_db.session.commit()
    return redirect(url_for("index"))

@app.route("/edit/<int:task_id>")
def edit(task_id):
    task = Task.query.filter_by(id=task_id).first()
    return render_template("edit.html", task=task)

@app.route("/delete/<int:task_id>")
def delete(task_id):
    task = Task.query.filter_by(id=task_id).first()
    task_db.session.delete(task)
    task_db.session.commit()
    return redirect(url_for("index"))

@app.route("/save/<int:task_id>", methods=["POST"])
def save(task_id):
    task = Task.query.filter_by(id=task_id).first()
    if request.method == "POST":
        edited_task_content = request.form.get("edited_task_content")
        if edited_task_content:
            task.content = edited_task_content # type: ignore
            task_db.session.commit()
    return redirect(url_for("index"))

@app.route("/cancel")
def cancel():
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)