from flask import Flask, render_template_string, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "your_secret_key"

# Database setup
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# User Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

with app.app_context():
    db.create_all()

base_css = """
<style>
    body { font-family: Arial, sans-serif; background: #f4f4f9; text-align: center; padding: 50px; }
    h2 { color: #333; }
    form { margin: 20px auto; width: 300px; }
    input { padding: 10px; margin: 10px 0; width: 100%; }
    button, a {
        background: #007bff; color: white; padding: 10px 20px;
        border: none; border-radius: 5px; cursor: pointer;
        text-decoration: none; display: inline-block; margin: 5px;
    }
    button:hover, a:hover { background: #0056b3; }
    table { margin: 20px auto; border-collapse: collapse; width: 80%; }
    th, td { border: 1px solid #ddd; padding: 10px; }
    th { background: #007bff; color: white; }
</style>
"""


@app.route("/")
def home():
    return render_template_string(base_css + """
        <h2>Welcome to Flask Auth App</h2>
        <a href='/signup'>Sign Up</a>
        <a href='/login'>Login</a>
    """)

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if User.query.filter_by(username=username).first():
            return "Username already exists!"

        hashed_pw = generate_password_hash(password)
        new_user = User(username=username, password=hashed_pw)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for("login"))

    return render_template_string(base_css + """
        <h2>Sign Up</h2>
        <form method="POST">
            <input type="text" name="username" placeholder="Username" required><br>
            <input type="password" name="password" placeholder="Password" required><br>
            <button type="submit">Sign Up</button>
        </form>
        <a href='/'>Back</a>
    """)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session["username"] = user.username
            return redirect(url_for("dashboard"))
        return "Invalid username or password!"

    return render_template_string(base_css + """
        <h2>Login</h2>
        <form method="POST">
            <input type="text" name="username" placeholder="Username" required><br>
            <input type="password" name="password" placeholder="Password" required><br>
            <button type="submit">Login</button>
        </form>
        <a href='/'>Back</a>
    """)

#  Dashboard 
@app.route("/dashboard")
def dashboard():
    if "username" not in session:
        return redirect(url_for("login"))
    return render_template_string(base_css + f"""
        <h2>Dashboard</h2>
        <p>Welcome, {session['username']}! You're logged in.</p>
        <a href='/view-users'>👥 View Users</a>
        <a href='/logout'>Logout</a>
    """)

@app.route("/view-users")
def view_users():
    if "username" not in session:
        return redirect(url_for("login"))
    all_users = User.query.all()
    return render_template_string(base_css + """
        <h2>Registered Users</h2>
        <table>
            <tr><th>ID</th><th>Username</th><th>Password Hash</th></tr>
            {% for user in users %}
                <tr><td>{{ user.id }}</td><td>{{ user.username }}</td><td>{{ user.password }}</td></tr>
            {% endfor %}
        </table>
        <a href='/dashboard'>Back to Dashboard</a>
    """, users=all_users)

@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)
