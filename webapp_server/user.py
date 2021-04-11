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