import geocoder
MAP_WIDTH = 1000
MAP_HEIGHT = 1000
MAX_SCORE = 100
SUM_AVG_WEIGHT = 33
class User: 
    def __init__(self, uid):
        self.uid = uid
        self.number_of_loc = 0
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
        print("AAA")

    def check_in(self):
        self.number_of_loc+=1

    def calculate_score(self):
        #cal server to get number and avg_score 
        self.score = self.score 
        

        

uid = 0

user = User(uid)
print(user)

