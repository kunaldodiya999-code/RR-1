from flask import render_template, request, redirect, session

USERNAME = "admin"
PASSWORD = "1234"

def auth_routes(app):

    @app.route("/")
    def home():
        if "user" in session:
            return redirect("/dashboard")
        return render_template("login.html")

    @app.route("/login", methods=["GET", "POST"])
    def login():
        if request.method == "POST":
            user = request.form.get("username")
            pwd = request.form.get("password")

            if user == USERNAME and pwd == PASSWORD:
                session["user"] = user
                return redirect("/fyers-login")   # ✅ IMPORTANT CHANGE

            return "Wrong Login"

        return render_template("login.html")   # ✅ Handles GET request

    @app.route("/logout")
    def logout():
        session.pop("user", None)
        session.pop("fyers_access_token", None)  # optional cleanup
        return redirect("/")
