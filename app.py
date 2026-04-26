from flask import Flask, render_template, request
from src.components.Clientdeets import clientmodif
from src.components.Employeedeets import employeemodif
import mysql.connector

app = Flask(__name__)

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="pashu",
        database="home_service"
    )

# -------------------- HOME PAGE --------------------
@app.route('/')
def home():
    return render_template("index.html")

# -------------------- MENU PAGES --------------------
@app.route('/signup-options')
def signup_options():
    return render_template("SignupOptions.html")

@app.route('/login-options')
def login_options():
    return render_template("LoginOptions.html")

# -------------------- SIGNUP PAGES --------------------
@app.route('/client-signup')
def client_signup():
    return render_template("ClientSignup.html")   # your existing client signup page

@app.route('/employee-signup')
def employee_signup():
    return render_template("EmployeeSignup.html") # your existing employee signup page

# -------------------- LOGIN PAGES --------------------
@app.route('/client-login')
def client_login():
    return render_template("ClientLogin.html")

@app.route('/employee-login')
def employee_login():
    return render_template("EmployeeLogin.html")

# -------------------- CLIENT SIGNUP SUBMIT --------------------
@app.route('/add-client', methods=['POST'])
def add_client():
    name = request.form.get("name")
    email = request.form.get("email")
    phone_num = request.form.get("phone_num").strip().replace(" ", "").replace("-", "")
    full_num = "+91" + phone_num
    lat = request.form.get("latitude")
    lng = request.form.get("longitude")

    conn = get_db_connection()
    cur = conn.cursor()

    query = "SELECT * FROM clients where email = %s AND phone_num = %s"
    cur.execute(query, (email, full_num))
    userexists = cur.fetchone()

    cur.close()
    conn.close()

    if userexists:
        return render_template("user_exists.html", login_url="/client-login", user_type="Client")

    else:
            
        clientmodif.AddClient(name, email, full_num, lat, lng)

        return "Client registered successfully!"

# -------------------- EMPLOYEE SIGNUP SUBMIT --------------------
@app.route('/add-employee', methods=['POST'])
def add_employee():
    name = request.form.get("name")
    email = request.form.get("email")
    phone_num = request.form.get("phone_num").strip().replace(" ", "").replace("-", "")
    full_num = "+91" + phone_num
    service = request.form.get("service")
    lat = request.form.get("latitude")
    lng = request.form.get("longitude")

    conn = get_db_connection()
    cur = conn.cursor()

    query = "SELECT * FROM clients where email = %s AND phone_num = %s"
    cur.execute(query, (email, full_num))
    userexists = cur.fetchone()

    cur.close()
    conn.close()

    if userexists:
        return render_template("user_exists.html", login_url="/employee-login", user_type="Employee")
    
    else:

        employeemodif.AddEmp(name, email, full_num, service, lat, lng)

        return "Employee registered successfully!"

# -------------------- CLIENT LOGIN VERIFY --------------------
@app.route('/verify-client-login', methods=['POST'])
def verify_client_login():
    email = request.form.get("email")
    phone_num = request.form.get("phone_num").strip().replace(" ", "").replace("-", "")

    if not phone_num.isdigit():
        return "Phone number must contain only digits."

    if len(phone_num) != 10:
        return "Phone number must be exactly 10 digits."

    full_phone = "+91" + phone_num

    conn = get_db_connection()
    cur = conn.cursor()

    query = "SELECT * FROM clients WHERE email = %s AND phone_num = %s"
    cur.execute(query, (email, full_phone))
    userexists = cur.fetchone()

    cur.close()
    conn.close()

    if userexists:
        return "Client login details verified successfully! (OTP comes next)"
    else:
        return "Client not found. Invalid email or phone number."

# -------------------- EMPLOYEE LOGIN VERIFY --------------------
@app.route('/verify-employee-login', methods=['POST'])
def verify_employee_login():
    email = request.form.get("email")
    phone_num = request.form.get("phone_num").strip().replace(" ", "").replace("-", "")

    if not phone_num.isdigit():
        return "Phone number must contain only digits."

    if len(phone_num) != 10:
        return "Phone number must be exactly 10 digits."

    full_phone = "+91" + phone_num

    conn = get_db_connection()
    cur = conn.cursor()

    query = "SELECT * FROM employees WHERE email = %s AND phone_num = %s"
    cur.execute(query, (email, full_phone))
    userexists = cur.fetchone()

    cur.close()
    conn.close()

    if userexists:
        return "Employee login details verified successfully! (OTP comes next)"
    else:
        return "Employee not found. Invalid email or phone number."

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)