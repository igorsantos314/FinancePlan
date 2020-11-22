from datetime import date
from os import path, mkdir
import shutil

class backup:

    def __init__(self):
        #DATA ATUAL
        self.day = date.today().day
        self.month = date.today().month
        self.year = date.today().year

        self.currentData = F'{self.day}-{self.month}-{self.year}'

        self.origem = 'finance.db'
        self.destino = F'/media/igor/Backup/{self.currentData}-finance.db'

    def createBackup(self):
        
        try:
            #REALIZAR BACKUP PARA UNIDADE REMOVIVEL
            shutil.copy(self.origem, self.destino)

            print(F'BACKUP DATA: {self.currentData} >> SUCESS !')
        
        except:
            print('ERROR BACKUP !')
        
#b = backup()


