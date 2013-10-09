from data.reader.DataReader import DiskDataReader
from rankclus.rankclus import RankClus
from rankclus.ranker import SimpleRanker
__author__ = 'haowu'

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
net = reader.read()
print net
ranker = SimpleRanker()
rc = RankClus(net,ranker,25)

# rc.initialization()
# rc.rank()
# rc.clustering()
# rc.adjust()
# rc.printResult()

rc.run()
rc.printResult(10)