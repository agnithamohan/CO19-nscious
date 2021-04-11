from flask import Flask, render_template, request, jsonify
from user import User
import json
import requests
import math

# TODO: Remove this list?
list_of_users = []
app = Flask(__name__)

users = {}
client_ip = 'http://127.0.0.1/5001'

MAP_WIDTH = 1000
MAP_HEIGHT = 1000
MAX_SCORE = 100
SUM_AVG_WEIGHT = 33  

MIN_COOR_X = 0 
MIN_COOR_Y = 0 
MAX_COOR_X = 4
MAX_COOR_Y = 4
SQUARE_SIDE = 1.2933
TOTAL_BOX_X = math.ceil(MAX_COOR_X/SQUARE_SIDE)
TOTAL_BOX_Y = math.ceil(MAX_COOR_Y/SQUARE_SIDE)
box_number_to_uid = {} # box to set

def get_bounding_box(location):
    # convert the latitud and longitude to a meter location 
    #the following is based on a meter location 
    # side of square 1.2933
    x = location[0]
    y = location[1]
    box_x = math.floor(x/SQUARE_SIDE)
    box_y = math.floor(y/SQUARE_SIDE)
    print(location, x, y)
    box_number = box_x*TOTAL_BOX_X + box_y
    return box_number

@app.route('/')
def index():
    menu = ['signup']
    return render_template('index.html', menu=menu)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        data = request.get_json() 
        username = data['username']
        location = data['location']
        location = location.strip(')(').split(', ')
        global MAP_WIDTH, MAP_HEIGHT
        x =  int(location[0])
        y =  int(location[1])
        global users, MAX_SCORE
        users[username] = User(username, MAX_SCORE, (x, y))
        print(users)
        return jsonify({"uid": username})
    return 'Done'

@app.route('/location', methods=['GET', 'POST'])
def location():
    headers = {'Content-Type': 'application/json'}
    ip = 'http://127.0.0.1:5001/location'
    r = requests.get(ip, headers=headers)
    location = r.json()['location']
    location = location.strip('()').split(', ')
    username = r.json()['username']
    box =  get_bounding_box([int(location[0]), int(location[1])])
    global users
    user = users[username]
    old_box = user.box
    if old_box != box: 
        global box_number_to_uid
        if old_box != -1:
            box_number_to_uid[old_box].remove(user.uid)
        if old_box not in box_number_to_uid.keys():
            box_number_to_uid[old_box] = set()
        if box not in box_number_to_uid.keys():
            box_number_to_uid[box] = set(user.uid)
    

    ## TODO: Should the score update be calculated here?
    user.update(location, user.score, box)
    users[username] = user
    print(users)
    return "ji"

# def add_user(uid, location):
#     user = User(uid, MAX_SCORE, location)
#     ind = len(list_of_users)
#     user.box = get_bounding_box(location)
#     list_of_users.append(user)
#     uid_to_index[uid] = ind
#     if user.box not in box_number_to_uid.keys():
#         box_number_to_uid[user.box] = set()
    
#     box_number_to_uid[user.box].add(uid)

def get_metrics(box_number):
    people = len(box_number_to_uid[box_number]) if box_number in box_number_to_uid.keys() else 0
    score = 0
    if people != 0:
        for p in box_number_to_uid[box_number]:
            ind = uid_to_index[p]
            score+=list_of_users[ind].score

    return people, score

@app.route('/get_crowd_metric', methods=['GET', 'POST'])
def get_crowd_metric():
    data = request.get_json() 
    location = data['location'].strip('()').split(', ')
    location[0] = int(location[0])
    location[1] = int(location[1])
    box_number = get_bounding_box(location)
    surrounding_boxes = []

    global TOTAL_BOX_X, TOTAL_BOX_Y

    # surrounding_boxes.append it 
    box_1 = box_number-TOTAL_BOX_X-1 # complicated
    box_2 = ((TOTAL_BOX_Y-1)*TOTAL_BOX_X)+box_number%TOTAL_BOX_X if box_number/TOTAL_BOX_Y == 0 else box_number-TOTAL_BOX_X
    box_3 = box_number-TOTAL_BOX_X+1 # complicated
    box_4 = box_number+TOTAL_BOX_X-1 if box_number%TOTAL_BOX_X == 0 else box_number - 1 
    box_5 = box_number-TOTAL_BOX_X-1 if (box_number+1)%TOTAL_BOX_X == 0 else box_number + 1 
    box_6 = box_number+TOTAL_BOX_X-1  # complicated
    box_7 = box_number%TOTAL_BOX_X if box_number/TOTAL_BOX_Y == 1 else box_number+TOTAL_BOX_X
    box_8 = box_number+TOTAL_BOX_X+1 # complicated
    box_9 = box_number

    surrounding_boxes.append(box_1)
    surrounding_boxes.append(box_2)
    surrounding_boxes.append(box_3)
    surrounding_boxes.append(box_4)
    surrounding_boxes.append(box_5)
    surrounding_boxes.append(box_6)
    surrounding_boxes.append(box_7)
    surrounding_boxes.append(box_8)
    surrounding_boxes.append(box_9)
    sum_people = 0.0
    sum_score = 0
    for box in surrounding_boxes: 
        print(box)
        n, s = get_metrics(box)
        sum_people += n 
        sum_score += s 

    avg = 100 if sum_people == 0 else sum_score/sum_people
    sum_people = 10 
    avg = 100
    data = {"people_sum": str(int(sum_people)), "score_avg": str(avg)}

    return jsonify(data)


# location = (0,2)
# uid = 0 
# add_user(uid, location)
# print(list_of_users)
# print(get_crowd_metric(2))