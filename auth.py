from flask import render_template, request, redirect, session

USERNAME = "admin"
PASSWORD = "1234"

def auth_routes(app):

    @app.route("/")
    def home():
        if "user" in session:
            return redirect("/dashboard")
        return render_template("login.html")

    @app.route("/login", methods=["POST"])
    def login():

        user = request.form["username"]
        pwd = request.form["password"]

        if user == USERNAME and pwd == PASSWORD:
            session["user"] = user
            return redirect("/dashboard")

        return "Wrong Login"

    @app.route("/logout")
    def logout():
        session.pop("user", None)
        return redirect("/")