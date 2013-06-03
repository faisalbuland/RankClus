__author__ = 'haowu'


class RankClus:
    def __init__(self,network,ranker,cluster):
        self.network = network
        self.ranker = ranker
        self.cluster - cluster

    def initialization(self):
        pass

    def rank(self):
        self.ranker.rank(self.network)

    def clustering(self):
        self.cluster.cluster(self.network)

    def adjust(self):
        pass

    def run(self):
        self.initialization()
        while True:
            self.rank()
            self.clustering()
            self.adjust()
            epsilon = 1





