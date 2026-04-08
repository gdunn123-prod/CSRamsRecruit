from flask import Flask, request, redirect, render_template_string, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import smtplib
from email.mime.text import MIMEText
import qrcode
import os

app = Flask(__name__)
app.secret_key = "csrams_secret_key"

# ======================
# DATABASE
# ======================
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ======================
# EMAIL FUNCTION
# ======================

def send_email(to_email, subject, html_message):
    sender_email = "your_email@gmail.com"
    app_password = "your_app_password"

    msg = MIMEText(html_message, "html")
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = to_email

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, app_password)
        server.send_message(msg)
        server.quit()
    except Exception as e:
        print("Email failed:", e)

# ======================
# MODELS
# ======================

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    email = db.Column(db.String(120), unique=True)
    phone = db.Column(db.String(20))
    parent_email = db.Column(db.String(120))
    interest = db.Column(db.String(100))
    location = db.Column(db.String(100))
    password = db.Column(db.String(200))

class Teacher(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(200))

# Create database + default teacher
with app.app_context():
    db.create_all()

    if not Teacher.query.filter_by(username="admin").first():
        teacher = Teacher(
            username="admin",
            password=generate_password_hash("admin123")
        )
        db.session.add(teacher)
        db.session.commit()

# ======================
# QR CODE (ONE-TIME GENERATION)
# ======================

url = "https://csramsrecruit.onrender.com/"

qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=4,
)
qr.add_data(url)
qr.make(fit=True)

img = qr.make_image(fill_color="black", back_color="white")
img.save("rams_recruit_qr.png")

print("QR code saved as rams_recruit_qr.png")

@app.route("/qrcode")
def generate_qr():
    url = "http://127.0.0.1:5000"

    img = qrcode.make(url)

    if not os.path.exists("static"):
        os.makedirs("static")

    img.save("static/site_qr.png")

    return """
    <h2>Scan to Visit RecruitCSRams</h2>
    <img src='/static/site_qr.png' width='300'>
    """

# ======================
# HOME PAGE
# ======================

@app.route("/")
def home():
    return render_template_string("""
    <html>
    <head>
        <title>CS & IT Program</title>
        <style>
            body {
                margin: 0;
                font-family: Arial, sans-serif;
                background: linear-gradient(
                    rgba(139,0,0,0.85),
                    rgba(139,0,0,0.85)
                ), url('/static/campus.jpg');
                background-size: cover;
                background-position: center;
                background-attachment: fixed;
                color: white;
                text-align: center;
            }
            .container {
                padding: 60px 20px;
                max-width: 1100px;
                margin: auto;
            }
            h1 { font-size: 3em; }
            p { font-size: 1.1em; line-height: 1.6; }

            .btn {
                display: inline-block;
                padding: 12px 25px;
                margin: 10px;
                background: white;
                color: #8B0000;
                text-decoration: none;
                border-radius: 25px;
                font-weight: bold;
            }

            .btn:hover { background: #ffe6e6; }

            .card {
                background: rgba(255,255,255,0.15);
                padding: 20px;
                border-radius: 15px;
                margin: 10px;
                display: inline-block;
                width: 260px;
            }

            .section {
                margin-top: 40px;
            }

            ul {
                text-align: left;
                display: inline-block;
            }
        </style>
    </head>

    <body>
        <div class="container">

            <h1>Computer Science & Information Technology Programs</h1>
            <p><b>Winston-Salem State University</b></p>
            <p>📞 336-750-2485 | ✉️ jonese@wssu.edu</p>

            <p>🚀 98% Employment Rate | 💻 Hands-On Learning | 🔐 Cybersecurity</p>

            <a href="/register" class="btn">Apply</a>
            <a href="/student_login" class="btn">Student Login</a>
            <a href="/login" class="btn">Teacher Login</a>

            <div class="section">
                <div class="card">💡 Innovative Learning</div>
                <div class="card">🔐 Cybersecurity Focus</div>
                <div class="card">🌐 Career Ready</div>
            </div>

            <div class="section">
                <h2>About the Program</h2>
                <p>
                Are you interested in gaming, social computing or virtual reality? 
                Do you think of yourself as a creative problem-solver?
                </p>
                <p>
                Earning a Master of Science in Computer Science and Information Technology 
                prepares you for careers in cybersecurity, software development, and research.
                </p>
                <p><b>98% of graduates</b> secure employment or continue education within 6 months.</p>
            </div>

            <div class="section">
                <h2>Program Options</h2>
                <div class="card">
                    <h3>5-Year B.S. → M.S.</h3>
                    <p>Earn both degrees faster and save time and money.</p>
                </div>
                <div class="card">
                    <h3>Data Analytics Certificate</h3>
                    <p>Great for any major entering tech.</p>
                </div>
            </div>

            <div class="section">
                <h2>Why Choose WSSU?</h2>
                <div class="card">#1 HBCU in NC</div>
                <div class="card">#1 for Social Mobility</div>
                <div class="card">Hands-on Internships</div>
                <div class="card">Faculty Mentorship</div>
            </div>

            <div class="section">
                <h2>Career Opportunities</h2>
                <ul>
                    <li>Software Developer</li>
                    <li>Cybersecurity Manager</li>
                    <li>Data Scientist</li>
                    <li>Network Architect</li>
                    <li>Database Administrator</li>
                    <li>Game Designer</li>
                </ul>
            </div>

            <div class="section">
                <h2>Info Session</h2>
                <p><b>April 1 @ 6:30 PM</b></p>
                <a href="/register" class="btn">Register Now</a>
            </div>

        </div>
    </body>
    </html>
    """)

# ======================
# RED STYLE TEMPLATE
# ======================

def red_style(content):
    return f"""
    <html>
    <head>
    <style>
        body {{
            font-family: Arial;
            background: #fff5f5;
            color: #8B0000;
            text-align: center;
        }}

        input, select {{
            padding: 10px;
            margin: 8px;
            border: 1px solid #8B0000;
            border-radius: 5px;
        }}

        button {{
            background: #8B0000;
            color: white;
            padding: 10px 20px;
            border-radius: 20px;
            border: none;
        }}

        table {{
            margin: auto;
            border-collapse: collapse;
        }}

        th, td {{
            border: 1px solid #8B0000;
            padding: 10px;
        }}
    </style>
    </head>
    <body>
    {content}
    </body>
    </html>
    """

# ======================
# STUDENT REGISTER
# ======================

@app.route("/register", methods=["GET","POST"])
def register():

    if request.method == "POST":

        # --- BASIC VALIDATION ---
        required_fields = ["first_name", "last_name", "email", "phone", "parent_email", "location", "password"]

        for field in required_fields:
            if not request.form.get(field):
                return red_style(f"""
                    <h3>Error: {field.replace('_',' ').title()} is required.</h3>
                    <a href='/register'>Go Back</a>
                """)

        # --- EMAIL ALREADY EXISTS ---
        existing = Student.query.filter_by(email=request.form["email"]).first()
        if existing:
            return red_style("""
                <h3>Email already registered!</h3>
                <a href='/student_login'>Login Instead</a>
            """)

        # --- PASSWORD LENGTH CHECK ---
        if len(request.form["password"]) < 6:
            return red_style("""
                <h3>Password must be at least 6 characters long.</h3>
                <a href='/register'>Go Back</a>
            """)

        # --- CREATE STUDENT ---
        student = Student(
            first_name=request.form["first_name"],
            last_name=request.form["last_name"],
            email=request.form["email"],
            phone=request.form["phone"],
            parent_email=request.form["parent_email"],
            interest=request.form["interest"],
            location=request.form["location"],
            password=generate_password_hash(request.form["password"])
        )

        db.session.add(student)
        db.session.commit()

        return redirect("/student_login")

    return red_style("""
    <h2>Register</h2>

    <form method="POST">
    <input name="first_name" placeholder="First Name"><br>
    <input name="last_name" placeholder="Last Name"><br>
    <input name="email" placeholder="Email"><br>
    <input name="phone" placeholder="Phone"><br>
    <input name="parent_email" placeholder="Parent Email"><br>
    <input name="location" placeholder="Location"><br>
    <input type="password" name="password" placeholder="Password"><br>

    <select name="interest">
        <option>Computer Science</option>
        <option>Information Technology</option>
        <option>Data Science</option>
        <option>Cybersecurity</option>
    </select><br><br>

    <button>Submit</button>
    </form>
    """)

# ======================
# STUDENT LOGIN
# ======================

@app.route("/student_login", methods=["GET","POST"])
def student_login():

    if request.method == "POST":
        student = Student.query.filter_by(email=request.form["email"]).first()

        if student and check_password_hash(student.password, request.form["password"]):
            session["student"] = student.id
            return redirect("/student_dashboard")

    return red_style("""
    <h2>Student Login</h2>

    <form method="POST">
    <input name="email" placeholder="Email"><br>
    <input type="password" name="password" placeholder="Password"><br>
    <button>Login</button>
    </form>
    """)

# ======================
# STUDENT DASHBOARD
# ======================

@app.route("/student_dashboard")
def student_dashboard():

    if "student" not in session:
        return redirect("/student_login")

    student = Student.query.get(session["student"])

    course_map = {
        "Computer Science": ["Algorithms", "Operating Systems", "Artificial Intelligence"],
        "Information Technology": ["Networking", "Cloud Computing", "System Administration"],
        "Data Science": ["Machine Learning", "Data Mining", "Data Visualization"],
        "Cybersecurity": ["Ethical Hacking", "Network Security", "Digital Forensics"]
    }

    recommended = course_map.get(student.interest, [])

    course_html = "".join([f"<li>{c}</li>" for c in recommended])

    return red_style(f"""
    <h2>Welcome {student.first_name}</h2>

    <p><b>Email:</b> {student.email}</p>
    <p><b>Interest:</b> {student.interest}</p>
    <p><b>Location:</b> {student.location}</p>

    <h3>Recommended Courses For You</h3>
    <ul>
    {course_html}
    </ul>

    <a href="/logout_student">Logout</a>
    """)

@app.route("/logout_student")
def logout_student():
    session.pop("student", None)
    return redirect("/")

# ======================
# TEACHER LOGIN
# ======================

@app.route("/login", methods=["GET","POST"])
def login():

    if request.method == "POST":
        user = Teacher.query.filter_by(username=request.form["username"]).first()

        if user and check_password_hash(user.password, request.form["password"]):
            session["user"] = user.username
            return redirect("/teacher")

    return red_style("""
    <h2>Teacher Login</h2>

    <form method="POST">
    <input name="username" placeholder="Username"><br>
    <input type="password" name="password" placeholder="Password"><br>
    <button>Login</button>
    </form>
    """)

# ======================
# TEACHER DASHBOARD
# ======================

@app.route("/teacher")
def teacher():

    if "user" not in session:
        return redirect("/login")

    students = Student.query.all()

    rows = ""
    for s in students:
        rows += f"""
        <tr>
            <td>{s.first_name} {s.last_name}</td>
            <td>{s.email}</td>
            <td>{s.parent_email}</td>
            <td>{s.interest}</td>
            <td>{s.location}</td>
            <td>
                <a href='/contact/{s.id}/student'>Email Student</a> |
                <a href='/contact/{s.id}/parent'>Email Parent</a> |
                <a href='/delete/{s.id}'>Delete</a>
            </td>
        </tr>
        """

    return red_style(f"""
    <h2>Teacher Dashboard</h2>

    <table>
    <tr>
        <th>Name</th>
        <th>Student Email</th>
        <th>Parent Email</th>
        <th>Interest</th>
        <th>Location</th>
        <th>Actions</th>
    </tr>
    {rows}
    </table>

    <br>
    <a href="/logout">Logout</a>
    """)

# ======================
# DELETE STUDENT (ADDED)
# ======================

@app.route("/delete/<int:id>")
def delete_student(id):

    if "user" not in session:
        return redirect("/login")

    student = Student.query.get_or_404(id)

    db.session.delete(student)
    db.session.commit()

    return red_style("""
        <h3>Student Deleted Successfully</h3>
        <a href='/teacher'>Back to Dashboard</a>
    """)

# ======================
# CONTACT STUDENT/PARENT
# ======================

@app.route("/contact/<int:id>/<type>", methods=["GET","POST"])
def contact(id, type):

    if "user" not in session:
        return redirect("/login")

    student = Student.query.get_or_404(id)

    email = student.email if type == "student" else student.parent_email

    if request.method == "POST":
        message = request.form["message"]

        send_email(email, "Message from WSSU CS Program", f"<p>{message}</p>")

        return red_style("""
        <h3>Email Sent Successfully</h3>
        <a href='/teacher'>Back to Dashboard</a>
        """)

    return red_style(f"""
    <h2>Send Email to {type.title()}</h2>
    <p><b>To:</b> {email}</p>

    <form method="POST">
        <textarea name="message" style="width:300px;height:150px;"></textarea><br><br>
        <button>Send Email</button>
    </form>
    """)

# ======================
# LOGOUT
# ======================

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

# ======================
# RUN APP
# ======================

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
