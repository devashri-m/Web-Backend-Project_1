from flask import Flask, request, session, abort, make_response, jsonify
import pymysql
from werkzeug.utils import secure_filename
import os
from flask_cors import CORS
import re
import jwt
from datetime import datetime, timedelta
from functools import wraps

app = Flask(__name__)

# CORS(app)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

upload_folder = 'C:/Users/macha/OneDrive - Cal State Fullerton/Documents/Web-backend/Project_1/upload_folder'
app.config["SECRET_KEY"] = 'af8d0c819f19479bb50f8e28c4b17f2c'
app.config['UPLOAD_PATH'] = upload_folder
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024
app.config['UPLOAD_EXTENSIONS'] = {'.jpeg', '.pdf', '.png'}

# To connect MySQL database
conn = pymysql.connect(
    host='localhost',
    user='root',
    password="apoorva",
    db='stress_detection_data',
    cursorclass=pymysql.cursors.DictCursor
)
cur = conn.cursor()

def token_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        token = extract_token(request)
        if not token:
            return token_missing_response()

        payload = decode_token(token)
        if not payload:
            return invalid_token_response()

        return func(*args, **kwargs)

    return decorated

def extract_token(req):
    token = None
    if "Authorization" in req.headers:
        data = req.headers["Authorization"]
        token = str.replace(str(data), "Bearer ", "")  # Token is extracted
    return token

def decode_token(token):
    try:
        payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])  #payload decoded from token
        return payload
    except jwt.ExpiredSignatureError:
        return None  # Token expired
    except jwt.InvalidTokenError:
        return None  # Invalid token

def token_missing_response():
    return make_response(jsonify({'Alert!': 'Token is missing', 'statusCode': 401}), 401)

def invalid_token_response():
    return make_response(jsonify({'Alert!': 'Token is invalid', 'statusCode': 401}), 401)



# To Register users with Email address and Password
@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        print('reached')
        email = request.form['email']
        password = request.form['password']

        cur.execute('SELECT * FROM users WHERE email = % s', (email,))
        user_email = cur.fetchone()
        print(user_email)
        conn.commit()
        if user_email:
            return abort(400, {'message': 'This Email is already in use!'})  # HTTP Bad Request Error Code 400
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            return abort(400, {'message': 'Invalid email address!'})
        elif not re.match(r'[A-Za-z0-9]+', password):
            return abort(400, {'message': 'Password must contain only characters and numbers'})
        else:
            cur.execute('INSERT INTO users VALUES (NULL, % s, % s)',
                        (email, password))
            conn.commit()
            msg = 'Your account have successfully created'
            response_code = 201  # HTTP Created 201 Status code
            return make_response(jsonify({'message': msg, 'statusCode': response_code}), 201)
    elif request.method == 'POST':
        return abort(400, {'message': 'Please register to create an account'})


# Login Users with Username and Password
@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']
        cur.execute('SELECT * FROM users WHERE email = % s AND password = % s', (email, password,))
        conn.commit()
        user = cur.fetchone()
        if user:
            session['loggedin'] = True
            # Create JWT for Login 
            token = jwt.encode({
                'email': email,
                'expiration': str(datetime.utcnow() + timedelta(minutes=15))
            }, app.config['SECRET_KEY'])

            msg = 'You are logged in successfully!'
            return jsonify({'token': token, 'message': msg})
        else:
            msg = 'Incorrect email / password !'
            return make_response({'message': msg}, 403, {'WWW-Authenticate': 'Basic realm: "Authentication Failed"'})


# Entered user details of their weekly schedule
@app.route('/user_details', methods=['POST'])
@token_required
def user_details():
    if request.method == 'POST' and 'name' in request.form and 'email' in request.form and 'exercise' in request.form and 'number_busy_week_days' in request.form and 'weekend_activity' in request.form:
        name = request.form['name']
        email = request.form['email']
        exercise = request.form['exercise']
        number_busy_week_days = request.form['number_busy_week_days']
        weekend_activity = request.form['weekend_activity']

        cur.execute('INSERT INTO user_schedule VALUES (NULL, % s, % s, % s, % s, % s)',
                    (name, email, exercise, number_busy_week_days, weekend_activity,))
        conn.commit()
        return make_response('Your schedule has been saved succcessfully', 201)
    else:
        return make_response('Invalid request fields', 400)


# Upload file for upload extensions 
@app.route('/upload', methods=['POST'])
@token_required
def upload():
    if request.method == 'POST':
        uploaded_file = request.files['file']
        filename = secure_filename(uploaded_file.filename)
        if filename != '':
            file_ext = os.path.splitext(filename)[1]
        if file_ext not in app.config['UPLOAD_EXTENSIONS']:
            print("unsuccessful")
            return make_response('Unsupported file extension', 400)
        uploaded_file.save(os.path.join(app.config['UPLOAD_PATH'], filename))
        return make_response('Upload Successful', 200)


@app.route('/public', methods=['GET'])
def public():
    return make_response('No Login is required here', 200)


# Request APTs in 5000 port with host=localhost
if __name__ == "__main__":
    app.run(host="localhost", port=int("5000"))