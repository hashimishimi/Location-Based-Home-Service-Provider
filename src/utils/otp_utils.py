import random


# -------------------- GENERATE OTP --------------------
def generate_otp():
    return str(random.randint(100000, 999999))


# -------------------- STORE OTP IN SESSION --------------------
def store_otp(session, otp, user_type, email, phone_num):

    session['otp'] = otp
    session['user_type'] = user_type
    session['email'] = email
    session['phone_num'] = phone_num


# -------------------- VERIFY OTP --------------------
def verify_user_otp(session, entered_otp):

    stored_otp = session.get("otp")

    return entered_otp == stored_otp


# -------------------- CLEAR OTP --------------------
def clear_otp(session):

    session.pop('otp', None)