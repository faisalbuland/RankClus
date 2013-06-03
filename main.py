from data.reader.DataReader import DiskDataReader

__author__ = 'haowu'

# ins = open("NetworkData/20090301_20090601.txt","r")
ins = open("NetworkData/test_list.txt","r")
list = []
for line in ins:
    line = line.strip()
    list.append(line)
ins.close()

reader = DiskDataReader("NetworkData/20090301_20090601",list)
net = reader.read()
print net