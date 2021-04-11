
import math

from user import User

list_of_users = []
test_loc = []
test_score = []
box_number_to_uid = {} # box to set
MIN_COOR_X = 0 
MIN_COOR_Y = 0 
MAX_COOR_X = 4
MAX_COOR_Y = 4
# SQUARE_SIDE = 1.2933
SQUARE_SIDE = 2
TOTAL_BOX_X = math.ceil(MAX_COOR_X/SQUARE_SIDE)
TOTAL_BOX_Y = math.ceil(MAX_COOR_Y/SQUARE_SIDE)
uid_to_index = {}
MAX_SCORE = 100

class User:
    def __init__(self, uid, score, location):
        self.uid = uid
        self.score = score
        self.location = location
        self.box = -1


    def __repr__(self): 
        return "UID:{uid} SCORE:{score} LOCATION:{loc} BOX:{box}".format(uid=self.uid, score=self.score, loc=self.location, box=self.box)
        
    def update(self, location, score, box):
        self.location = location
        self.score = score
        self.box = box

    

def get_bounding_box(location):
    # convert the latitud and longitude to a meter location 
    #the following is based on a meter location 
    # side of square 1.2933
    x = location[0]
    y = location[1]
    box_x = math.floor(x/SQUARE_SIDE)
    box_y = math.floor(y/SQUARE_SIDE)
    box_number = box_x*TOTAL_BOX_X + box_y
    return box_number


# run this periodically and update 
def get_locations():
    for i in range(len(list_of_users)):
        #make http call to the client and get location
        user = list_of_users[i]
        location =  test_loc[i]
        score = test_score[i]
        box =  get_bounding_box(location)
        old_box = user.box
        if old_box != box: 
            box_number_to_uid[old_box].remove(user.uid)
            if user.box not in box_number_to_uid.keys():
                box_number_to_uid[user.box] = set()
            box_number_to_uid[box].add(user.uid)
        user.update(location, score, box)


def add_user(uid, location):
    user = User(uid, MAX_SCORE, location)
    ind = len(list_of_users)
    user.box = get_bounding_box(location)
    list_of_users.append(user)
    uid_to_index[uid] = ind
    if user.box not in box_number_to_uid.keys():
        box_number_to_uid[user.box] = set()
    
    box_number_to_uid[user.box].add(uid)


def get_metrics(box_number):
    people = len(box_number_to_uid[box_number]) if box_number in box_number_to_uid.keys() else 0
    score = 0
    if people != 0:
        for p in box_number_to_uid[box_number]:
            ind = uid_to_index[p]
            score+=list_of_users[ind].score

    return people, score

# function to get number of people and score
# 1 2 3 
# 4 * 5 
# 6 7 8 
def get_crowd_metric(box_number):
    surrounding_boxes = []
    print(TOTAL_BOX_X)
    print(TOTAL_BOX_Y)

    # surrounding_boxes.append it 
    box_1 = box_number-TOTAL_BOX_X-1 # complicated
    box_2 = ((TOTAL_BOX_Y-1)*TOTAL_BOX_X)+box_number%TOTAL_BOX_X if box_number/TOTAL_BOX_Y == 0 else box_number-TOTAL_BOX_X
    box_3 = box_number-TOTAL_BOX_X+1 # complicated
    box_4 = box_number+TOTAL_BOX_X-1 if box_number%TOTAL_BOX_X == 0 else box_number - 1 
    box_5 = box_number-TOTAL_BOX_X-1 if (box_number+1)%TOTAL_BOX_X == 0 else box_number + 1 
    box_6 = box_number+TOTAL_BOX_X-1  # complicated
    box_7 = box_number%TOTAL_BOX_X if box_number/TOTAL_BOX_Y == 1 else box_number+TOTAL_BOX_X
    box_8 = box_number+TOTAL_BOX_X+1 # complicated

    surrounding_boxes.append(box_1)
    surrounding_boxes.append(box_2)
    surrounding_boxes.append(box_3)
    surrounding_boxes.append(box_4)
    surrounding_boxes.append(box_5)
    surrounding_boxes.append(box_6)
    surrounding_boxes.append(box_7)
    surrounding_boxes.append(box_8)
    sum_people = 0.0
    sum_score = 0.0
    # print("ddd")
    # print(box_1)
    # print(box_2)
    # print(box_3)
    # print(box_4)
    # print(box_5)
    # print(box_6)
    # print(box_7)
    # print(box_8)
    for box in surrounding_boxes: 
        print(box)
        n, s = get_metrics(box)
        # print("ko")
        # print(n, s)
        sum_people += n 
        sum_score += s 

    avg = 100 if sum_people == 0 else sum_score/sum_people
    return sum_people, avg


location = (0,2)
uid = 0 
add_user(uid, location)
print(list_of_users)
print(get_crowd_metric(2))