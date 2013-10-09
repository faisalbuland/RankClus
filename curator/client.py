__author__ = 'haowu'

from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from cogcomp.curator.Curator import *



class curatorClient:
    def __init__(self,add = "trollope.cs.illinois.edu" ,port = 9010):

        """
        :param add: ie. # trollope.cs.illinois.edu
        :param port:  ie #9010
        """
        try:
            self.transport = TSocket.TSocket(add, port)
            self.transport = TTransport.TFramedTransport(self.transport)
            self.protocol = TBinaryProtocol.TBinaryProtocol(self.transport)
            self.client = Client(self.protocol)

        except Thrift.TException, tx:
            print tx

    def getRecord(self,text,type,forceUpdate):
        """
        get record from curator
        :param text: Text to processe
        :param type: type of service ie. "ner" "wikifier"
        :param forceUpdate: boolean flag
        """
        # self.transport.open()
        msg = self.client.provide(type,text,forceUpdate)
        # self.transport.close()
        return msg

    def open(self):
        self.transport.open()

    def close(self):
        self.transport.close()

