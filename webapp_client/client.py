from flask import Flask, render_template, request, jsonify
from user import User
import requests
import json
import geocoder

app = Flask(__name__)
uid = None
user_obj = None
server_ip = 'http://127.0.0.1:5000'

MAP_WIDTH = 1000
MAP_HEIGHT = 1000
MAX_SCORE = 100
SUM_AVG_WEIGHT = 33 

@app.route('/')
def index():
    menu = ['signup']
    return render_template('index.html', menu=menu)

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     error = None
#     if request.method == 'POST':
#         if valid_login(request.form['username'],
#                        request.form['password']):
#             return log_the_user_in(request.form['username'])
#         else:
#             error = 'Invalid username/password'
#     return render_template('login.html', error=error)

# @app.route('/profile')
# def profile():
#     return render_template('profile.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        data = request.get_json() 
        # username = data['username']
        username = request.form['username']
        location = geocoder.ip('me').latlng
        x =  (int) ((MAP_WIDTH/360.0) * (180 + location[1]))
        y =  (int) ((MAP_HEIGHT/180.0) * (90 - location[0]))
        headers = {'Content-Type': 'application/json'}
        send_data = {"username":username, "location":repr((x, y))}
        r = requests.post('http://127.0.0.1:5000/signup', data=json.dumps(send_data), headers=headers)
        global uid, user_obj
        uid = r.json()['uid']
        user_obj = User(uid)
    # return 'done'
    return render_template('signup.html')

@app.route('/location', methods=['GET', 'POST'])
def location():
    if request.method == 'GET':
        global user_obj
        user_obj.update_location()
        location = user_obj.get_location()
        send_data = {"username":user_obj.uid, "location":repr(location)}
        return jsonify(send_data)
    return "Done"

@app.route('/score', methods=['GET', 'POST'])
def score():
    if request.method == 'GET':
        global user_obj
        user_obj.calculate_score()
        score = user_obj.get_score()
        d = {"score" : str(score), "rating" : str(5.0*score/100.0), "uid": user_obj.uid}
    # return d
    return render_template('profile.html', data=d)