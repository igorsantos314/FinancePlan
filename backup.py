from datetime import date
from os import path, mkdir

class backup:

    def __init__(self):
        #DATA ATUAL
        self.day = date.today().day
        self.month = date.today().month
        self.year = date.today().year

        self.currentData = F'{self.day}.{self.month}.{self.year}'

    def createDirBackup(self):

        if path.exists(self.currentData):
            print('Backup Exist')

        else:
            mkdir(F'BACKUP-{self.currentData}')

    
        

b = backup()
b.createDirBackup()

