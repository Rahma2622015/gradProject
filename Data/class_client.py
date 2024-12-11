from Data.dataStorage import DataStorage
import time


class Client:

    def __init__(self):
        self.id=None
        self.timeStart= None
        self.timeEnd= None
        self.last_task = None
        self.data=DataStorage()


    def setClientId(self,id):
        self.id=id


    def getClientId(self):
        return self.id


    def data_storage(self,key ,value):
        if self.data.addData(key,value):
            return True
        return False


    def startSession(self,id):
        self.timeStart = time.time()
        self.id=id
        self.timeEnd= self.timeStart + 1000
        if time.time() >= self.timeEnd:
            return False
        return True


    def endSession(self)->bool:
        if self.timeEnd is None:
            return False
        if time.time() >= self.timeEnd:
            return True
        return False


    def __repr__(self):
        return f"Client(Data={self.data})"