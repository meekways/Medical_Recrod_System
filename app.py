from flask import Flask, redirect, render_template, request, url_for
from flask_bootstrap import Bootstrap
# from flask_wtf import FlaskForm

app = Flask(__name__)
Bootstrap(app)


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/login/", methods=["GET", "POST"])
def login():
    return render_template("login.html", name="login")

@app.route("/registration/", methods=["GET", "POST"])
def registration():
    return render_template("registration.html", name="registration")


# @app.route("/users/", methods=["GET", "POST"])
# def users():
#     return render_template("users.html")
        

if __name__ == "__main__":
    app.run(debug=True)