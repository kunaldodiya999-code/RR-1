from flask import Flask, redirect, request, session
from auth import auth_routes
from trades import trade_routes
from database import init_db
import os

app = Flask(__name__)
app.secret_key = "rrmonitorsecret"

init_db()

auth_routes(app)
trade_routes(app)


@app.route("/")
def root():
    if "user" in session:
        return redirect("/dashboard")
    return redirect("/login")


@app.route("/fyers-login")
def fyers_login():
    from fyers_apiv3 import fyersModel

    app_id = os.getenv("FYERS_APP_ID")
    secret_key = os.getenv("FYERS_SECRET_KEY")
    redirect_uri = os.getenv("FYERS_REDIRECT_URI")

    fyers = fyersModel.SessionModel(
        client_id=app_id,
        secret_key=secret_key,
        redirect_uri=redirect_uri,
        response_type="code",
        grant_type="authorization_code"
    )

    auth_url = fyers.generate_authcode()
    return redirect(auth_url)


@app.route("/fyers-callback")
def fyers_callback():
    from fyers_apiv3 import fyersModel

    auth_code = request.args.get("auth_code")

    if not auth_code:
        return "No auth_code received."

    app_id = os.getenv("FYERS_APP_ID")
    secret_key = os.getenv("FYERS_SECRET_KEY")
    redirect_uri = os.getenv("FYERS_REDIRECT_URI")

    fyers = fyersModel.SessionModel(
        client_id=app_id,
        secret_key=secret_key,
        redirect_uri=redirect_uri,
        response_type="code",
        grant_type="authorization_code"
    )

    fyers.set_token(auth_code)

    token_response = fyers.generate_token()

    if token_response.get("s") == "ok":
        session["fyers_access_token"] = token_response["access_token"]
        session["fyers_refresh_token"] = token_response["refresh_token"]

        return redirect("/dashboard")

    return f"FYERS Login Failed: {token_response}"


if __name__ == "__main__":
    app.run()