from flask import Flask, g, render_template, request, flash, session, redirect, url_for
import sqlite3


app = Flask(__name__)
app.secret_key = "53VtZY-hhSnq23ehlA4WmA"
DATABASE = "user_credentials.db"


def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


@app.route("/")
def display_main_page():
    return render_template("login.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        if "username" in request.form and "password" in request.form:
            username = request.form["username"]
            password = request.form["password"]
            db = get_db()
            cursor = db.cursor()
            cursor.execute("SELECT * FROM user WHERE username='" + username + "' AND password='" + password + "'")
            # correct implementation to eliminate SQL Injection vulnerability:
            # cursor.execute("SELECT * FROM user WHERE username=? AND password=?", (username, password))
            info = cursor.fetchone()
            if info is None:
                error = "Credentials not matching"
            else:
                session["user"] = username
                return redirect(url_for("display_profile"))
    return render_template("login.html", error=error)


@app.route("/register", methods=["GET", "POST"])
def register():
    error = None
    if request.method == "POST":
        if "" in [request.form["username"], request.form["firstname"], request.form["surname"],
                  request.form["password"], request.form["r_password"]]:
            error = "Fill in all the fields and try again"
        else:
            username = request.form["username"]
            db = get_db()
            cursor = db.cursor()
            cursor.execute("SELECT username FROM user WHERE username=?", (username,))
            info = cursor.fetchone()
            if info is not None:
                error = "Username already exists"
            else:
                password = request.form["password"]
                r_password = request.form["r_password"]
                if password != r_password:
                    error = "Passwords do not match!"
                else:
                    firstname = request.form["firstname"]
                    surname = request.form["surname"]
                    cursor.execute("""
                    CREATE TABLE IF NOT EXISTS user(
                    userID INTEGER PRIMARY KEY,
                    username VARCHAR(20) NOT NULL,
                    firstname VARCHAR(20) NOT NULL,
                    surname VARCHAR(20) NOT NULL,
                    password VARCHAR(40) NOT NULL);
                    """)
                    cursor.execute("""
                    INSERT INTO user(username, firstname, surname, password)
                    VALUES(?, ?, ?, ?)
                    """, (username, firstname, surname, password))
                    db.commit()
                    flash("Profile has been successfully created")
                    session["user"] = username
                    return redirect(url_for("display_profile"))
    return render_template("register.html", error=error)


@app.route("/profile")
def display_profile():
    if "user" in session:
        user = session["user"]
        flash(f"You are currently logged in as {user}.")
        return render_template('profile.html')
    return redirect(url_for("login"))


@app.route("/logout")
def logout():
    session.pop("user", None)
    flash("You have successfully logged out")
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)
