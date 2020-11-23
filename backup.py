from datetime import date
from os import path, mkdir, listdir
import shutil
import getpass

class backup:

    def __init__(self):
        #DATA ATUAL
        self.day = date.today().day
        self.month = date.today().month
        self.year = date.today().year

        self.currentData = F'{self.day}-{self.month}-{self.year}'

        self.origem = 'finance.db'
        
    def createBackup(self, device):

        #PEGA O NOME DO USUARIO ATUAL
        user = getpass.getuser()

        self.destino = F'/media/{user}/{device}/{self.currentData}-finance.db'

        try:
            #REALIZAR BACKUP PARA UNIDADE REMOVIVEL
            shutil.copy(self.origem, self.destino)
        
        except:
            pass
    
    def getDevices(self):
        #LISTA DIR DE DEVICES
        return listdir('/media/igor/')
        
#b = backup()