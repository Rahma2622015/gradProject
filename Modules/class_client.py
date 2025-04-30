from Modules.dataStorage import DataStorage
import time


class Client:

    def __init__(self):
        self.__id = None
        self.timeStart= None
        self.timeEnd= None
        self.last_task = None
        self.data=DataStorage()


    def setClientId(self,id):
        self.__id=id

    def data_storage(self,key ,value):
        if self.data.addData(key,value):
            return True
        return False


    def startSession(self,id):
        self.timeStart = time.time()
        self.id=id
        self.timeEnd= self.timeStart + 60000
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
        return f"Client(ID={self.id}, Data={self.data})"
