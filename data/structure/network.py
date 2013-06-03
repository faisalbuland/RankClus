__author__ = 'haowu'
import numpy as np
import random


def chunks(l, k):
    """ Yield successive n-sized chunks from l.
    :param l: list to chunk
    :param n: chunk num
    """
    ret = []
    for i in range(k):
        ret.append([])
    idx = 0
    for x in l:
        ret[idx].append(x)
        idx = (idx + 1) % k
    return ret



class Network:
    def __init__(self,matrixs,nodes):
        """
        :param matrixs: numpy matrix objects in array  [self.Wxx,self.Wxy,self.Wyx,self.Wyy]
                        so the whole matrix looks like
                        Wxx Wxy
                        Wyx Wyy
                        that is really the edges of the graph
        :param nodes:   detail information of nodes
                        ie. the text info of nodes
                            the detail info of users
                        Since it is an bi-type network
                        we made it as an array of [X,Y]

        :param k:       the clustering number
        """
        [self.Wxx,self.Wxy,self.Wyx,self.Wyy] = matrixs
        self.weight = np.bmat([[self.Wxx, self.Wxy], [self.Wyx, self.Wyy]])
        self.nodes = nodes


    def getSubGraph(self,t):
        """
        :return: the subgraph giving cluster# t
                in format of [wxx,wxy,wyx,wyy]
                the size won't change,since other wise we will lost idx info.
        """

        subNodes = self.cluster[t]
        subM = len(subNodes)
        m = len(self.Wxx)
        n = len(self.Wyy)

        wxx = np.zeros((m,m))
        wxy = np.zeros((m,n))
        wyx = np.zeros((n,m))
        wyy = np.zeros((n,n))

        for idx in subNodes:
            wxx[:,idx] = self.Wxx[:,idx]
            wxy[idx,1:] = self.Wxx[idx,1:]
            wyx[:,idx] = self.Wxx[:,idx]

        wyy=self.Wyy



        return [wxx,wxy,wyx,wyy]



    def init_cluster(self,k):
        """
        init the cluster
        need to make sure no cluster is empty after calling this function
        if k is larger than the size of nodes, raise Error
        """
        self.k = k

        # find out thread count
        m = len(self.Wxx)
        tmp_list=[]

        for i in range(0,m):
            tmp_list.append(i)
            # self.cluster.append([])
        # shuffle
        random.shuffle(tmp_list)
        # chunk into clustering
        self.cluster = chunks(tmp_list,k)



    def getClusterCenters(self):
        """
        :return: an array of size k, i-th entry is the center of i-th cluster
        """
        return None

    def rank(self):
        pass

    def getNodesInfo(self,idx):
        """

        :param idx: the idx of node you want
        :return: return the ifo of idx-th node
        """
        return None


    def __repr__(self):
        """
        :return: return the deatil info of the network
        """
        return self.__str__()

    def __str__(self):
        ret = "Matrix:\n"+ str(self.weight)+"\n"
        helperText = "in WYY, Wyy[i][j] is how many times user i is quoting user j (i reply to j)"
        return ret+helperText


