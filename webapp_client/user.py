import geocoder
import requests
import json

MAP_WIDTH = 1000
MAP_HEIGHT = 1000
MAX_SCORE = 100
SUM_AVG_WEIGHT = 33

class User: 
    def __init__(self, uid):
        self.uid = uid
        self.number_of_loc = 7
        self.location = (0, 0)
        self.score = MAX_SCORE
        self.update_location()

    def update_location(self):
        g = geocoder.ip('me')
        g = g.latlng
        x =  (int) ((MAP_WIDTH/360.0) * (180 + g[1]))
        y =  (int) ((MAP_HEIGHT/180.0) * (90 - g[0]))
        self.location = (x,y)

    def __repr__(self): 
        return "UID:{uid} SCORE:{score} LOCATION:{loc}".format(uid=self.uid, score=self.score, loc=self.location)

    def register(self): 
        #send server your details: 
        print("HAVE NOT IMPLEMENTED")

    def get_location(self):
        return self.location

    def get_score(self):
        return self.score

    def check_in(self):
        self.number_of_loc+=1

    def calculate_score(self):
        headers = {'Content-Type': 'application/json'}
        print("Locationjkk: ", repr(self.location))

        data = {"location":repr(self.location)}
        people_score = requests.get("http://127.0.0.1:5000/get_crowd_metric", data=json.dumps(data),headers=headers)
        print("people_sCOre" , people_score.json())
        res = people_score.json()

        WEIGHT_SELF = 1
        WEIGHT_PEOPLE = 0.09
        WEIGHT_SCORE = 0.13
        WEIGHT_LOC = 0.13
        # update the self.score here bSased on weighted values. 
        self.score = WEIGHT_SELF * self.score - WEIGHT_PEOPLE * int(res['people_sum']) - WEIGHT_SCORE * (self.score - float(res['score_avg'])) - WEIGHT_LOC * self.number_of_loc
        self.score = min(100, self.score)

        # self.score = self.score 