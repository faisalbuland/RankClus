from data.structure.network import ClusterEmptyError

__author__ = 'haowu'

import numpy as np


class RankClus:
    def __init__(self,network,ranker,k):
        """

        Basic setup of the framework.

        This class is just an interface, all the real thing are done in Network class


        :param network: the network data
        :param ranker: the ranking interface
        :param clusterMethod: the cluster method
        :param k: k cluster number
        """
        self.network = network
        self.ranker = ranker
        self.k = k

    def initialization(self):
        """
        initialization of the network, Step 0
        """
        self.network.init_cluster(self.k)


    def rank(self):
        """
        rank each sub-graph. Setp 1
        """
        self.network.rank(self.ranker)

    def clustering(self):
        """
        Calculated clustering center. Step 2

        """
        # self.cluster.cluster(self.network)
        self.network.estimateParameter()
        self.network.do_cluster()
    def adjust(self):
        """

        Adjust the network. Step 3
        """
        return self.network.adjustCluster()

    def run(self):
        """
        Standard workflow.
        See the framework section of the paper (RankClus: Integrating Clustering with Ranking for Heterogeneous Information Network Analysis, Yizhou Sun, Jiawei han et al. 2009) for detail

        """
        self.initialization()

        retryTimes = 0
        it =0
        while True:
            it +=1
            try:
                print "ITERATION %s",it
                self.rank()
            except ClusterEmptyError,e:
                print "Empty cluster detected!!"
                print "Re-run initialization"
                self.initialization()
                it = 0
                retryTimes +=1
                if retryTimes > 5:
                    print "already re-init 5 times, still have empty cluster"
                    print "Please examine your data or configs"
                    break

                continue
            print "ITERATION %s",it
            self.clustering()

            epsilon = self.adjust()
            if it>10 or epsilon < 0.05:
                break

        # print self.network.__str__()


    def printResult(self,limit=None):
        self.network.clusterView(limit)




