import mysql.connector
from geopy.distance import geodesic

def get_db_connection():

    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="pashu",
        database="home_service"
    )


# -------------------- CREATE SERVICE REQUEST --------------------
def create_service_request(client_ID, service_name):

    conn = get_db_connection()
    cur = conn.cursor()

    # get client location
    cur.execute(
        "SELECT lat, lng FROM clients WHERE client_ID = %s",
        (client_ID,)
    )

    location = cur.fetchone()

    lat = location[0]
    lng = location[1]

    # insert request
    cur.execute("""
        INSERT INTO service_requests
        (client_ID, service_name, lat, lng)

        VALUES (%s, %s, %s, %s)
    """, (client_ID, service_name, lat, lng))

    conn.commit()

    cur.close()
    conn.close()


# -------------------- GET EMPLOYEE SERVICE --------------------
def get_employee_service(emp_ID):

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(
        "SELECT service FROM employees WHERE emp_ID = %s",
        (emp_ID,)
    )

    employee = cur.fetchone()

    cur.close()
    conn.close()

    return employee[0]


# -------------------- GET PENDING REQUESTS --------------------
def get_pending_requests(service_name, emp_ID, radius_km=10):

    conn = get_db_connection()
    cur = conn.cursor()

    # get employee location
    cur.execute("""
        SELECT lat, lng

        FROM employees

        WHERE emp_ID = %s
    """, (emp_ID,))

    employee_location = cur.fetchone()

    emp_lat = employee_location[0]
    emp_lng = employee_location[1]

    # get matching pending requests
    cur.execute("""
        SELECT *

        FROM service_requests

        WHERE service_name = %s
        AND status = 'Pending'
    """, (service_name,))

    requests = cur.fetchall()

    nearby_requests = []

    # filter by distance
    for request in requests:

        request_lat = request[3]
        request_lng = request[4]

        employee_coords = (emp_lat, emp_lng)
        request_coords = (request_lat, request_lng)

        distance = geodesic(
            employee_coords,
            request_coords
        ).km

        if distance <= radius_km:

            nearby_requests.append(request)

    cur.close()
    conn.close()

    return nearby_requests


# -------------------- ACCEPT REQUEST --------------------
def accept_service_request(request_id, emp_ID):

    conn = get_db_connection()
    cur = conn.cursor()

    # get request + client details
    cur.execute("""
        SELECT
            sr.lat,
            sr.lng,
            sr.service_name,
            c.phone_num

        FROM service_requests sr

        JOIN clients c
            ON sr.client_ID = c.client_ID

        WHERE sr.request_id = %s
    """, (request_id,))

    request_data = cur.fetchone()

    lat = request_data[0]
    lng = request_data[1]
    service_name = request_data[2]
    client_phone = request_data[3]

    # update request
    cur.execute("""
        UPDATE service_requests

        SET status = 'Accepted',
            assigned_emp_ID = %s

        WHERE request_id = %s
    """, (emp_ID, request_id))

    conn.commit()

    cur.close()
    conn.close()

    # terminal output
    print("\n==================================")
    print("REQUEST ACCEPTED")
    print(f"Employee ID: {emp_ID}")
    print(f"Service: {service_name}")
    print()
    print("Client Location:")
    print("Google Maps:")
    print(f"https://www.google.com/maps?q={lat},{lng}")
    print()
    print("Client Contact Number:")
    print(f"Client Phone: {client_phone}")
    print("==================================\n")



# -------------------- GET ACCEPTED REQUESTS --------------------
def get_accepted_requests(emp_ID):

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT *

        FROM service_requests

        WHERE assigned_emp_ID = %s
        AND status = 'Accepted'
    """, (emp_ID,))

    requests = cur.fetchall()

    cur.close()
    conn.close()

    return requests


# -------------------- CLOSE REQUEST --------------------
def close_request(request_id):

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        UPDATE service_requests

        SET status = 'Closed'

        WHERE request_id = %s
    """, (request_id,))

    conn.commit()

    cur.close()
    conn.close()


# -------------------- COMPLETE REQUEST --------------------
def complete_request(request_id):

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        UPDATE service_requests

        SET status = 'Completed'

        WHERE request_id = %s
    """, (request_id,))

    conn.commit()

    cur.close()
    conn.close()