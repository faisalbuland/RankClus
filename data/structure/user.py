__author__ = 'haowu'

class ForumUser:
    def __init__(self,userID):
        self.userID = userID
        self.cited = []
        self.posts = []

    def __eq__(self, other):
        return self.userID == other.userID

