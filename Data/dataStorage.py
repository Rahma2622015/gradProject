class DataStorage:

    def __init__(self):
        self.data = dict()

    def addData(self, name, value):
        if name not in self.data:
            self.data[name] = value
            return True
        return False

    def findName(self, name):
        return name in self.data

    def findValue(self,value):
        return value in self.data.values()

    def fetchName(self,value):
        for item in self.data.items():
            if item[1] == value:
                return item
        else :
            return False

    def fetchValue(self,name):
        for key,value in self.data.items():
            if name == key:
                return value
        return False

    def updateData(self,name,newValue):
        if self.findName(name):
            self.data[name] = newValue
            return True
        return False

    def deleteData(self,name):
        if self.findName(name):
            self.data.pop(name)
            return True
        return False

    def __str__(self):
        return str(self.data)

