__author__ = 'haowu'
import json
import numpy as np

from data.structure.network import Network


def removeNonAscii(s): return "".join(filter(lambda x: ord(x) < 128, s))


def cleanDic(obj):
    for key in obj.keys():
        if key == "time" or type(key) == int or key == "intTime" or key == "postID":
            continue
        obj[key] = removeNonAscii(obj[key])


class DataReader:
    """ An Data Reader interface"""

    def __init__(self):
        pass

    def read(self):
        """
        read data, and should RETURN the NETWORK
        """
        pass

    def getData(self):
        """

        Return the data that has already been read.
        """
        pass


class DiskDataReader(DataReader):
    """
    An Data Reader read from disk
    each thread will be in one file
    each file should be an array of json obj
    """

    def __init__(self, rootPath, fileList):
        """

        :param rootPath: the root of all files
        :param fileList: the filelist
        """
        DataReader.__init__(self)
        self.root = rootPath
        self.fileList = fileList

    def read(self):
        """
        read data from file and then parse it for threads and user

        """
        self.threads = {}
        self.user = {}
        for file in self.fileList:
            ins = open(self.root + "/" + file, "r")
            obj = json.loads(ins.read())
            if not obj[0]['postID'] == 1:
                # if is is not started from the day, just ignore it
                continue
            else:
                # else just
                self.threads[obj[0]['threadID']] = obj
            ins.close()
            for post in obj:

                cleanDic(post)
                cited = ""
                if post['quote'] == "":
                    pass
                else:

                    quote = str(removeNonAscii(post['quote']))
                    try:
                        idx = quote.index(":")
                        # sanity check of the data
                        quote.index("Originally posted by ")

                        quote = quote[:idx]
                        if "Originally posted by " in quote:
                            cited = quote.replace("Originally posted by ", "")
                            # print cited
                    except ValueError, e:
                        #if error rasied, means data needs to clean
                        # ie. wrong format of quoting text
                        # we need to go through all posts to look posts
                        q = list(obj).index(post)
                        for i in range(q - 1, -1, -1):
                            if str(post['quote']) in str(obj[i]['reply']):
                                cited = obj[i]['userID']
                post['quoteUserId'] = cited
                # print post['userID'],"->",cited

        # now we need to parse the data into matrix
        # X type denote to posts, and Y type denotes to User
        # first build an index table for threads and users

        threadTable = []
        userTable = []
        for key in self.threads.keys():
            threadTable.append(key)
            for post in self.threads[key]:
                if not post['userID'] in userTable:
                    userTable.append(post['userID'])

        # now we have table with their indexs, each entry of those two table are ensure unique

        # m is the |x| and n is |y|
        # x is threads and y is users, posts are links
        m = len(threadTable)
        n = len(userTable)

        # looks at the __init__ function of network to see specification
        wxx = np.zeros((m, m))
        wxy = np.zeros((m, n))
        wyx = np.zeros((n, m))
        wyy = np.zeros((n, n))

        #go over threads and posts and generated the 4 matrix.
        for i in range(0, m):
            threadID = threadTable[i]
            thread = self.threads[threadID]
            NumPost = len(thread)
            wxx[i][i] += NumPost
            for post in thread:
                postUser = post['userID']
                j = userTable.index(postUser)
                wyx[j][i] += 1
                wxy[i][j] += 1
                replyUser = post['quoteUserId']
                if replyUser == "":
                    pass
                else:
                    try:
                        k = userTable.index(replyUser)
                        wyy[j][k] += 1
                    except ValueError,e:
                        replyUser = ""


        # now we have the network, construct it



        matrix = [wxx, wxy, wyx, wyy]
        # print matrix
        for i in range(len(threadTable)):
            tid = threadTable[i]
            title_x = self.threads[tid][0]['title']
            obj_to_add = {"tid":tid,"Title":title_x}
            threadTable[i]=obj_to_add



        network = Network(matrix, [threadTable, userTable])

        return network


    def resolveReply(self):
        pass

    def getData(self):
        pass