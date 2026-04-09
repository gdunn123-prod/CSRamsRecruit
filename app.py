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
    checked_in = db.Column(db.Boolean, default=False)   # event check-in
    applied = db.Column(db.Boolean, default=False)      # optional: later mark as applicant

class Teacher(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(200))

class Session(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))

class Attendance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'))
    session_id = db.Column(db.Integer, db.ForeignKey('session.id'))

# Create database + default teacher + some default sessions
with app.app_context():
    db.create_all()

    if not Teacher.query.filter_by(username="admin").first():
        teacher = Teacher(
            username="admin",
            password=generate_password_hash("admin123")
        )
        db.session.add(teacher)
        db.session.commit()

    # Default sessions for the Open House
    default_sessions = ["Welcome & Overview", "Cybersecurity Demo", "AI & Data Science", "Student Panel"]
    for sname in default_sessions:
        if not Session.query.filter_by(name=sname).first():
            db.session.add(Session(name=sname))
    db.session.commit()

# ======================
# STATIC SITE QR (GENERAL)
# ======================

@app.route("/qrcode")
def generate_qr():
    url = "https://csramsrecruit.onrender.com/"  # change if needed

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

            @media (max-width: 600px) {
                h1 { font-size: 2.2em; }
                .card { width: 90%; }
                .btn { width: 80%; }
            }
        </style>
    </head>

    <body>
        <div class="container">

            <h1>Computer Science & Information Technology Programs</h1>
            <p style="font-size: 16px; opacity: 0.9; margin-top: 8px;">Explore the Computer Science & IT Program at Winston-Salem State University</p>
            <p><b>Winston-Salem State University</b></p>
            <p>📞 336-750-2485 | ✉️ jonese@wssu.edu</p>

            <p>🚀 98% Employment Rate | 💻 Hands-On Learning | 🔐 Cybersecurity</p>

            <a href="/register" class="btn">Apply / Register</a>
            <a href="/student_login" class="btn">Student Login</a>
            <a href="/login" class="btn">Faculty Login</a>

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
            padding: 20px;
        }}

        input, select, textarea {{
            padding: 10px;
            margin: 8px;
            border: 1px solid #8B0000;
            border-radius: 5px;
            width: 260px;
            max-width: 90%;
        }}

        button {{
            background: #8B0000;
            color: white;
            padding: 10px 20px;
            border-radius: 20px;
            border: none;
            cursor: pointer;
        }}

        button:hover {{
            background: #a80000;
        }}

        table {{
            margin: auto;
            border-collapse: collapse;
            width: 95%;
            max-width: 900px;
        }}

        th, td {{
            border: 1px solid #8B0000;
            padding: 8px;
            font-size: 14px;
        }}

        th {{
            background: #fbe3e3;
        }}

        a {{
            color: #8B0000;
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

        existing = Student.query.filter_by(email=request.form["email"]).first()

        if existing:
            return red_style("""
            <h3>Email already registered!</h3>
            <a href='/student_login'>Login Instead</a>
            """)

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

        # Generate unique QR code for student check-in
        qr_url = f"https://csramsrecruit.onrender.com/checkin/{student.id}"

        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(qr_url)
        qr.make(fit=True)

        if not os.path.exists("static/qr"):
            os.makedirs("static/qr")

        qr_img = qr.make_image(fill_color="black", back_color="white")
        qr_img.save(f"static/qr/student_{student.id}.png")

        # Simple automated follow-up email after registration
        email_body = f"""
        <h2>Thank you for registering, {student.first_name}!</h2>
        <p>We’re excited to see you at the CS & IT Open House.</p>
        <p><b>Interest Area:</b> {student.interest}</p>
        <p>Bring this email with you and check in using your QR code at the event.</p>
        """
        send_email(student.email, "WSSU CS Open House Registration", email_body)

        return redirect("/student_login")

    return red_style("""
    <h2>Open House Registration</h2>

    <form method="POST">
    <input name="first_name" placeholder="First Name" required><br>
    <input name="last_name" placeholder="Last Name" required><br>
    <input name="email" placeholder="Email" type="email" required><br>
    <input name="phone" placeholder="Phone"><br>
    <input name="parent_email" placeholder="Parent Email" type="email"><br>
    <input name="location" placeholder="Location"><br>
    <input type="password" name="password" placeholder="Password" required><br>

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

    # Simple "schedule" = list of sessions
    sessions = Session.query.all()
    session_html = "".join([f"<li>{s.name}</li>" for s in sessions])

    checked_text = "Yes" if student.checked_in else "Not yet"

    return red_style(f"""
    <h2>Welcome {student.first_name}</h2>

    <p><b>Email:</b> {student.email}</p>
    <p><b>Interest:</b> {student.interest}</p>
    <p><b>Location:</b> {student.location}</p>
    <p><b>Event Check-In:</b> {checked_text}</p>

    <h3>Your Check-In QR Code</h3>
    <p>Show this at the event to be checked in.</p>
    <img src="/static/qr/student_{student.id}.png" width="200" alt="Student QR Code">

    <h3>Recommended Courses For You</h3>
    <ul>
    {course_html}
    </ul>

    <h3>Sample Open House Schedule</h3>
    <ul>
    {session_html}
    </ul>

    <a href="/logout_student">Logout</a>
    """)

@app.route("/logout_student")
def logout_student():
    session.pop("student", None)
    return redirect("/")

# ======================
# QR CHECK-IN
# ======================

@app.route("/checkin/<int:id>")
def checkin(id):
    student = Student.query.get_or_404(id)
    student.checked_in = True
    db.session.commit()

    return red_style(f"""
    <h2>Welcome, {student.first_name}!</h2>
    <p>You are now <b>checked in</b> for the CS Open House.</p>
    <p>Enjoy the sessions and feel free to ask questions!</p>
    """)

# ======================
# SESSION CHECK-IN (PER SESSION)
# ======================

@app.route("/session_qr/<int:session_id>")
def session_qr(session_id):
    """Generate a QR code for a specific session (for admins to print)."""
    sess = Session.query.get_or_404(session_id)
    url = f"https://csramsrecruit.onrender.com/session_checkin/{session_id}"

    if not os.path.exists("static/session_qr"):
        os.makedirs("static/session_qr")

    img = qrcode.make(url)
    img.save(f"static/session_qr/session_{session_id}.png")

    return red_style(f"""
    <h2>QR Code for Session: {sess.name}</h2>
    <img src="/static/session_qr/session_{session_id}.png" width="250" alt="Session QR">
    """)

@app.route("/session_checkin/<int:session_id>")
def session_checkin(session_id):
    """When scanned at a session, student enters email to mark attendance."""
    sess = Session.query.get_or_404(session_id)

    return red_style(f"""
    <h2>Session Check-In: {sess.name}</h2>
    <p>Enter your email to record your attendance.</p>
    <form method="POST" action="/session_checkin_submit/{session_id}">
        <input name="email" placeholder="Your Email" type="email" required><br>
        <button>Check In</button>
    </form>
    """)

@app.route("/session_checkin_submit/<int:session_id>", methods=["POST"])
def session_checkin_submit(session_id):
    sess = Session.query.get_or_404(session_id)
    email = request.form["email"]
    student = Student.query.filter_by(email=email).first()

    if not student:
        return red_style("""
        <h3>Email not found.</h3>
        <p>Please register first or check your spelling.</p>
        <a href="/">Back to Home</a>
        """)

    # Record attendance if not already recorded
    existing = Attendance.query.filter_by(student_id=student.id, session_id=session_id).first()
    if not existing:
        db.session.add(Attendance(student_id=student.id, session_id=session_id))
        db.session.commit()

    return red_style(f"""
    <h2>Thank you, {student.first_name}!</h2>
    <p>Your attendance has been recorded for <b>{sess.name}</b>.</p>
    """)

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
# TEACHER DASHBOARD WITH ANALYTICS
# ======================

@app.route("/teacher")
def teacher():

    if "user" not in session:
        return redirect("/login")

    students = Student.query.all()
    total_students = len(students)
    total_checked_in = Student.query.filter_by(checked_in=True).count()

    # Simple "conversion": checked-in / registered
    conversion_rate = 0
    if total_students > 0:
        conversion_rate = round((total_checked_in / total_students) * 100, 1)

    # Interest breakdown
    interest_counts = {}
    for s in students:
        interest_counts[s.interest] = interest_counts.get(s.interest, 0) + 1

    interest_html = "".join([f"<li>{k}: {v}</li>" for k, v in interest_counts.items()])

    # Session popularity
    sessions = Session.query.all()
    session_rows = ""
    for sess in sessions:
        count = Attendance.query.filter_by(session_id=sess.id).count()
        session_rows += f"<tr><td>{sess.name}</td><td>{count}</td><td><a href='/session_qr/{sess.id}'>View QR</a></td></tr>"

    # Student table
    rows = ""
    for s in students:
        status = "Checked In" if s.checked_in else "Not Checked In"
        rows += f"""
        <tr>
            <td>{s.first_name} {s.last_name}</td>
            <td>{s.email}</td>
            <td>{s.parent_email}</td>
            <td>{s.interest}</td>
            <td>{s.location}</td>
            <td>{status}</td>
            <td>
                <a href='/contact/{s.id}/student'>Email Student</a> |
                <a href='/contact/{s.id}/parent'>Email Parent</a> |
                <a href='/delete/{s.id}'>Delete</a>
            </td>
        </tr>
        """

    return red_style(f"""
    <h2>Teacher Dashboard</h2>

    <h3>Recruitment Analytics</h3>
    <p><b>Total Registrations:</b> {total_students}</p>
    <p><b>Total Checked In:</b> {total_checked_in}</p>
    <p><b>Conversion (Registered → Checked In):</b> {conversion_rate}%</p>

    <h4>Interest Breakdown</h4>
    <ul>
        {interest_html}
    </ul>

    <h4>Session Popularity</h4>
    <table>
        <tr>
            <th>Session</th>
            <th>Attendance Count</th>
            <th>QR Code</th>
        </tr>
        {session_rows}
    </table>

    <h3>Registered Students</h3>
    <table>
    <tr>
        <th>Name</th>
        <th>Student Email</th>
        <th>Parent Email</th>
        <th>Interest</th>
        <th>Location</th>
        <th>Check-In Status</th>
        <th>Actions</th>
    </tr>
    {rows}
    </table>

    <br>
    <a href="/logout">Logout</a>
    """)

# ======================
# CONTACT / EMAIL
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
# DELETE STUDENT
# ======================

@app.route("/delete/<int:id>")
def delete(id):
    if "user" not in session:
        return redirect("/login")

    student = Student.query.get_or_404(id)
    db.session.delete(student)
    db.session.commit()

    return redirect("/teacher")

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

