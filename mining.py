from cogcomp.base.ttypes import Labeling, AnnotationFailedException
from curator.client import curatorClient

__author__ = 'haowu'

import json
import os

def removeNonAscii(s): return "".join(filter(lambda x: ord(x) < 128, s))


def cleanDic(obj):
    for key in obj.keys():
        if key == "time" or type(key) == int or key == "intTime" or key == "postID":
            continue
        obj[key] = removeNonAscii(obj[key])


class DiskDataReader:
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
                        q = obj.index(post)
                        for i in range(q - 1, -1, -1):
                            if str(post['quote']) in str(obj[i]['reply']):
                                cited = obj[i]['userID']
                post['quoteUserId'] = cited
                # print post['userID'],"->",cited

        # now we need to parse the data into matrix
        # X type denote to posts, and Y type denotes to User
        # first build an index table for threads and users
        return self.threads

class wikifer:
    def __init__(self,threads):
        self.threads = threads
        self.curatorClient = curatorClient()
        self.readParsedKey()


    def wikify(self):
        count = 0
        for key in self.threads.keys():
            filename = key+".json"
            count +=1
            print filename
            print "%s of %s" % (count,len(self.threads.keys()))
            if filename not in self.done:
                pass
            else:
                continue

            ts = self.threads[key]
            to_write = []
            self.curatorClient.open()
            for post in ts:
                content = post['reply']
                try:
                    reco = self.curatorClient.getRecord(content,"wikifier",False)
                except AnnotationFailedException,e:
                    continue
                obj = {}
                obj['postID'] = post['postID']
                obj['entity'] = []
                spans = reco.labelViews.get('wikifier').labels
                for span in spans:
                    url = span.label
                    if url == "UNMAPPED":
                        continue
                    entity = url[str(url).rindex("/")+1:]
                    obj['entity'].append(entity)
                    #print entity
                to_write.append(obj)


            ins = open("mining_out/"+filename,"w+")
            ins.write(json.dumps(to_write,sort_keys=True, indent=4))
            ins.close()
            self.curatorClient.close()


    def readParsedKey(self):
        self.done = []
        files = os.listdir("mining_out")
        self.done = files


ins = open("NetworkData/20090301_20090601.txt","r")

# ins = open("NetworkData/test_list.txt","r")
list = []
for line in ins:
    line = line.strip()
    if line.startswith("#"):
        continue
    list.append(line)
ins.close()

reader = DiskDataReader("NetworkData/20090301_20090601",list)
# ins = open("NetworkData/test_list.txt","r")

threads = reader.read()
wk = wikifer(threads)
wk.wikify()


# ccg = curatorClient()
#
# reco = ccg.getRecord("Hello Obama","wikifier",False)
# spans = reco.labelViews.get('wikifier').labels
# for span in spans:
#     url = span.label
#     entity = url[str(url).rindex("/")+1:]
#     print entity

# print spans
# print type(reco.labelViews['wikifier'])