from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"
app.config["SECRET_KEY"] = "8f685354dfd4c4130ad282f2d113355c151b9d676872b7be91e2fabd4c34be65"

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager()
login_manager.init_app(app)

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

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# AUTH APP ROUTES
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("username")
        if username and password:
            existing_user = User.query.filter_by(username=username).first()
            if existing_user:
                return redirect(url_for("uae.html"))
            else:
                hashed_password = bcrypt.generate_password_hash(password)
                new_user = User(username=username, password=hashed_password)
                db.session.add(new_user)
                db.session.commit()
                return redirect(url_for("login"))
    return render_template("register.html")

    # when user clicks this,
    # if POST, get the username and password inputted
    #   if username was entered: 
    #       check User db to see if username exists in User db
    #       if username does not exist,
    #           if password was entered:
    #               create password hash
    #               create instance of User class and assign the username and password
    #               add that instance to the db
    #               commit session
    #       else(username exists):
    #           redirect to uae.html
    #           

@app.route("/login")
def login():
    return render_template("login.html")

# register
# login
# logout



# TASK APP ROUTES
@app.route("/home")
def home():
    tasks = Task.query.all()
    print(tasks)
    return render_template("home.html", tasks=tasks)

@app.route("/add", methods=["POST"])
def add():
    task_content = request.form.get("task_content")
    new_task = Task(content=task_content, status=False) # type: ignore
    db.session.add(new_task)
    db.session.commit()
    return redirect(url_for("home"))

@app.route("/update/<int:task_id>")
def update(task_id): 
    task = Task.query.filter_by(id=task_id).first()
    task.status = not task.status # type: ignore
    db.session.commit()
    return redirect(url_for("home"))

@app.route("/edit/<int:task_id>")
def edit(task_id):
    task = Task.query.filter_by(id=task_id).first()
    return render_template("edit.html", task=task)

@app.route("/delete/<int:task_id>")
def delete(task_id):
    task = Task.query.filter_by(id=task_id).first()
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for("home"))

@app.route("/save/<int:task_id>", methods=["POST"])
def save(task_id):
    task = Task.query.filter_by(id=task_id).first()
    if request.method == "POST":
        edited_task_content = request.form.get("edited_task_content")
        if edited_task_content:
            task.content = edited_task_content # type: ignore
            db.session.commit()
    return redirect(url_for("home"))

@app.route("/cancel")
def cancel():
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)