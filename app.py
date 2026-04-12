from flask import Flask, render_template, request
from src.components.Clientdeets import clientmodif
from src.components.Employeedeets import employeemodif

app = Flask(__name__)

# Main page
@app.route('/')
def home():
    return render_template("index.html")

# Client page
@app.route('/client-signup')
def client_login():
    return render_template("ClientSignup.html")

# Employee page
@app.route('/employee-signup')
def employee_login():
    return render_template("EmployeeSignup.html")

# Client submit
@app.route('/add-client', methods=['POST'])
def add_client():
    name = request.form.get("name")
    email = request.form.get("email")
    phone_num = request.form.get("phone_num")
    lat = request.form.get("latitude")
    lng = request.form.get("longitude")

    clientmodif.AddClient(name, email, phone_num, lat, lng)

    return "Client added successfully!"

# Employee submit
@app.route('/add-employee', methods=['POST'])
def add_employee():
    name = request.form.get("name")
    email = request.form.get("email")
    phone_num = request.form.get("phone_num")
    lat = request.form.get("latitude")
    lng = request.form.get("longitude")
    service = request.form.get("service")

    employeemodif.AddEmp(name, email, phone_num, service, lat, lng,)

    return "Employee added successfully!"

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)