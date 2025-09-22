from flask import Flask, render_template, request, redirect, url_for, session, flash
import pickle, pandas as pd
from utils.email_utils import mail, generate_otp, send_otp_email
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "supersecretkey"

# Mail config
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = "your_email@gmail.com"
app.config['MAIL_PASSWORD'] = "your_app_password"
mail.init_app(app)

# DB config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    dob = db.Column(db.String(20))
    email = db.Column(db.String(100), unique=True)
    mobile = db.Column(db.String(20))
    verified = db.Column(db.Boolean, default=False)

db.create_all()

model = pickle.load(open("mental_health_model.pkl", "rb"))

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        session["name"] = request.form["name"]
        session["dob"] = request.form["dob"]
        session["email"] = request.form["email"]
        session["mobile"] = request.form["mobile"]
        otp = generate_otp()
        session["otp"] = otp
        send_otp_email(app, session["email"], otp)
        flash("OTP sent to your email. Please verify.")
        return redirect(url_for("verify"))
    return render_template("signup.html")

@app.route("/verify", methods=["GET", "POST"])
def verify():
    if request.method == "POST":
        entered_otp = request.form["otp"]
        if entered_otp == session.get("otp"):
            user = User(name=session["name"], dob=session["dob"], email=session["email"], mobile=session["mobile"], verified=True)
            db.session.add(user)
            db.session.commit()
            flash("Email verified successfully!")
            return redirect(url_for("dashboard"))
        else:
            flash("Invalid OTP. Please try again.")
            return redirect(url_for("verify"))
    return render_template("verify.html")

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html", name=session.get("name"))

@app.route("/profile", methods=["GET", "POST"])
def profile():
    if request.method == "POST":
        session["sleep_hours"] = int(request.form["sleep_hours"])
        session["food_quality"] = int(request.form["food_quality"])
        session["exercise_hours"] = int(request.form["exercise_hours"])
        session["work_stress"] = int(request.form["work_stress"])
        session["screen_time"] = int(request.form["screen_time"])
        session["health_issues"] = int(request.form["health_issues"])
        session["introvert_extrovert"] = request.form["introvert_extrovert"]
        return redirect(url_for("check"))
    return render_template("profile.html")

@app.route("/check")
def check():
    return render_template("check.html")

@app.route("/result", methods=["POST"])
def result():
    input_data = {
        "sleep_hours": session["sleep_hours"],
        "food_quality": session["food_quality"],
        "exercise_hours": session["exercise_hours"],
        "work_stress": session["work_stress"],
        "screen_time": session["screen_time"],
        "health_issues": session["health_issues"],
        "introvert_extrovert": session["introvert_extrovert"]
    }
    df = pd.DataFrame([input_data])
    df = pd.get_dummies(df, drop_first=True)
    model_features = model.feature_names_in_
    for col in model_features:
        if col not in df.columns:
            df[col] = 0
    df = df[model_features]
    prediction = model.predict(df)[0]
    advice = {
        "stressed": "Try relaxation exercises and take short breaks.",
        "anxious": "Practice mindfulness and avoid excessive screen time.",
        "depressed": "Please consult a therapist for proper guidance.",
        "happy": "Keep up your healthy lifestyle!",
        "stable": "Maintain your balance and self-care routine."
    }
    return render_template("result.html", prediction=prediction, advice=advice[prediction])

if __name__ == "__main__":
    app.run(debug=True)
