import sqlite3
import os

class bd:

    def __init__(self):

        #LISTA DE MESES
        self.months = ['JANEIRO', 'FEVEREIRO', 'MARCO', 'ABRIL', 'MAIO', 'JUNHO', 'JULHO', 'AGOSTO', 'SETEMBRO', 'OUTUBRO', 'NOVEMBRO', 'DEZEMBRO']

        caminhoAtual = os.getcwd()

        self.conection = sqlite3.connect('{}/finance.db'.format(caminhoAtual))
        self.cur = self.conection.cursor()
    
    def createTablesMonths(self, m):
        #CRIAR TABELAS DE MESES
        command = 'CREATE TABLE {} (ID INTEGER, ano TEXT, Item TEXT, valor REAL, status Text)'.format(m)
        
        self.cur.execute(command)
        self.conection.commit()

    def getLastID(self, m, y):
        
        #PEGA A LISTA DE GASTOS
        gastos = self.getListaGastosMes(m, y)

        #VERIFICA SE É NULA
        if len(gastos) == 0:
            return 0

        else:
            #RETORNA O NOVO ID
            return int(gastos[-1][0]) + 1 

    def getNameMonth(self, m):
        #TRANSFORMA MES DE NUMERO PARA O NOME
        return self.months[m-1]

    def insertItem(self, m, ano, Item, valor, status):
        
        #PEGA O UTLIMO INDICE
        ind = self.getLastID(m, ano)

        #INSERIR DADOS NA TABELA MES NA POSICAO M
        command = f'INSERT INTO {self.getNameMonth(m)} (ID, ano, Item, valor, status) VALUES({ind}, "{ano}", "{Item}", {valor}, "{status}")'
        print(command)

        self.cur.execute(command)
        self.conection.commit()

    def getListaGastosMes(self, m, y):

        #EXIBIR TODOS OS DADOS DE UMA TABELA MES, PELA DATA ESPECIFICA
        show = f"SELECT * FROM {self.getNameMonth(m)} WHERE ano = '{y}'"

        self.cur.execute(show)
        gastos = self.cur.fetchall()

        #RETORNA A SOMA DOS VALORES DO MES E ANO DESEJADOS
        return gastos

    def getGastosMes(self, m, y):

        #EXIBIR TODOS OS DADOS DE UMA TABELA MES, PELA DATA ESPECIFICA
        show = f"SELECT valor FROM {self.getNameMonth(m)} WHERE ano = '{y}'"

        self.cur.execute(show)
        valores = self.cur.fetchall()

        #RETORNA A SOMA DOS VALORES DO MES E ANO DESEJADOS
        return sum([v[0] for v in valores])

    def dropDespesa(self, m, ind):

        #DELETAR DESPESA
        command = f'DELETE FROM {self.getNameMonth(m)} WHERE id = {ind}'

        self.cur.execute(command)
        self.conection.commit()

    def resetDataBase(self):
        
        for m in range(13):
            
            #EXIBIR TODOS OS DADOS DE UMA TABELA MES, PELA DATA ESPECIFICA
            show = f"SELECT ID FROM {self.getNameMonth(m)}"

            self.cur.execute(show)
            valores = self.cur.fetchall()
            
            for i in valores:
                self.dropDespesa(m, i[0])

a = bd()
#for i in a.months:
#    a.createTablesMonths(i)
#b.resetDataBase()