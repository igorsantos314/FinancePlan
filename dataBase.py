import sqlite3
import os
import csv
from datetime import date

class bd:

    def __init__(self):

        #DATA ATUAL
        self.day = date.today().day
        self.month = date.today().month
        self.year = date.today().year

        self.currentData = F'{self.day}/{self.month}/{self.year}'

        #LISTA DE MESES
        self.months = ['JANEIRO', 'FEVEREIRO', 'MARCO', 'ABRIL', 'MAIO', 'JUNHO', 'JULHO', 'AGOSTO', 'SETEMBRO', 'OUTUBRO', 'NOVEMBRO', 'DEZEMBRO']

        #TIPO DE GASTOS
        self.spendings = ('ALIMENTACAO', 'COMBUSTIVEL', 'CARTAO -', 'SAUDE', 'TRANSPORTE', 'MTL', 'OUTROS')
        self.revenues = ('TRABALHO', 'PROEJETO', 'DESENV.', 'ESCOLA', 'INVESTIMENTOS', 'OUTROS')

        caminhoAtual = os.getcwd()

        self.conection = sqlite3.connect('{}/finance.db'.format(caminhoAtual))
        self.cur = self.conection.cursor()

    # ----------------------------------- CRIAÇÃO DE TABELAS -----------------------------------
    def createTablesMonths(self, m):
        #CRIAR TABELAS DE MESES
        command = 'CREATE TABLE {} (ID INTEGER, ano TEXT, Item TEXT, valor REAL, status Text)'.format(m)
        
        self.cur.execute(command)
        self.conection.commit()

    def createTablesBoxs(self, b):

        #CRIAR TABELAS DE BOXs
        command = F'CREATE TABLE BOX{b} (ID INTEGER, data TEXT, Item TEXT, valor REAL)'
        
        self.cur.execute(command)
        self.conection.commit()

    def createTablesBoxT(self):

        #CRIAR TABELAS DE BOXs
        command = 'CREATE TABLE BOXT (ID INTEGER, mes TEXT, ano TEXT, Item TEXT, valor REAL, status Text)'
        
        self.cur.execute(command)
        self.conection.commit()

    def createTableLog(self):
        #CRIAR TABELAS DE LOG
        command = 'CREATE TABLE LOG (data TEXT, action TEXT)'
        
        self.cur.execute(command)
        self.conection.commit()

    def createTableInvestments(self):
        #CRIAR TABELAS DE INVESTIMENTOS
        command = 'CREATE TABLE INVESTMENTS (Id INTEGER, data TEXT, nome_ativo TEXT, tipo_ativo TEXT, tipo_transacao TEXT, valor REAL, quant_ativos INTEGER, numero_estados INTEGER, taxa_adm REAL)'
        
        self.cur.execute(command)
        self.conection.commit()

    # ----------------------------------- INSERIR NA BASE DE DADOS -----------------------------------
    def insertLog(self, data, action):
        pass
        #INSERIR NOVO LOG
        #command = f'INSERT INTO LOG (data, action) VALUES("{data}", "{action}")'

        #self.cur.execute(command)
        #self.conection.commit()

    def insertBox(self, box, data, Item, valor):

        #PEGA O UTLIMO INDICE
        ind = self.getLastIDBox(box)

        #INSERIR DADOS NA TABELA MES NA POSICAO M
        command = f'INSERT INTO BOX{box} (ID, data, Item, valor) VALUES({ind}, "{data}", "{Item}", {valor})'
        
        #LOG
        self.insertLog(self.currentData, F'INSERT DATA IN BOX {box}')

        self.cur.execute(command)
        self.conection.commit()

    def insertBoxT(self, mes, ano, Item, valor, status):

        #PEGA O UTLIMO INDICE
        ind = self.getLastIDBox('T')

        #INSERIR DADOS NA TABELA MES NA POSICAO M
        command = f'INSERT INTO BOXT (ID, mes, ano, Item, valor, status) VALUES({ind}, "{mes}", "{ano}", "{Item}", {valor}, "{status}")'
        
        #LOG
        self.insertLog(self.currentData, F'INSERT DATA IN BOX T')

        self.cur.execute(command)
        self.conection.commit()

    def insertItem(self, m, ano, Item, valor, status):
        
        #PEGA O UTLIMO INDICE
        ind = self.getLastID(m, ano)

        #INSERIR DADOS NA TABELA MES NA POSICAO M
        command = f'INSERT INTO {self.getNameMonth(m)} (ID, ano, Item, valor, status) VALUES({ind}, "{ano}", "{Item}", {valor}, "{status}")'

        self.cur.execute(command)
        self.conection.commit()

        #LOG
        self.insertLog(self.currentData, F'INSERT EM BOX T IN MONTH {m}')

    def insertInvestment(self, data, nome_ativo, tipo_ativo, tipo_transacao, valor, quant_ativos, numero_estados, taxa_adm):
        #PEGA O UTLIMO INDICE
        ind = self.getLastIdInvestments()

        #INSERIR DADOS NA TABELA MES NA POSICAO M
        command = f'INSERT INTO INVESTMENTS (Id, data, nome_ativo, tipo_ativo, tipo_transacao, valor, quant_ativos, numero_estados, taxa_adm) VALUES({ind}, "{data}", "{nome_ativo}", "{tipo_ativo}", "{tipo_transacao}", {valor}, {quant_ativos}, {numero_estados}, {taxa_adm})'

        self.cur.execute(command)
        self.conection.commit()

    # ----------------------------------- SETOR DE CONSULTA -----------------------------------
    def getListBox(self, box):

        #EXIBIR TODOS OS DADOS DE UMA TABELA MES, PELA DATA ESPECIFICA
        show = f"SELECT * FROM BOX{box}"

        self.cur.execute(show)
        BOXs = self.cur.fetchall()

        #RETORNA A SOMA DOS VALORES DO MES E ANO DESEJADOS
        return BOXs

    def getListBoxTCurrent(self, m, y):
        
        #EXIBIR TODOS OS DADOS DE UMA TABELA MES, PELA DATA ESPECIFICA
        show = f"SELECT * FROM BOXT where mes='{m}' AND ano='{y}'"

        self.cur.execute(show)
        boxT = self.cur.fetchall()

        #RETORNA A SOMA DOS VALORES DO MES E ANO DESEJADOS
        return boxT

    def getSumBox(self, box):

        #EXIBIR TODOS OS DADOS DA CAIXA SELECIONADA
        show = f"SELECT valor FROM BOX{box}"

        self.cur.execute(show)
        BOXs = self.cur.fetchall()

        #RETORNA A SOMA DOS VALORES
        return sum( [ i[0] for i in BOXs] )

    def getSumBoxT(self, m, y):

        #EXIBIR TODOS OS DADOS DA CAIXA SELECIONADA
        show = f"SELECT valor FROM BOXT WHERE mes='{m}' AND ano='{y}' AND status='PG'"

        self.cur.execute(show)
        BOXs = self.cur.fetchall()

        #RETORNA A SOMA DOS VALORES
        return sum( [ i[0] for i in BOXs] )

    def getInvestments(self):
        #EXIBIR TODOS OS INVESTIMENTOS
        show = f"SELECT * FROM INVESTMENTS"

        self.cur.execute(show)
        inv = self.cur.fetchall()

        #RETORNA TODOS OS INVESTIMENTOS
        return inv

    def getLastIDBox(self, box):

        #LISTA CASH DEPOSIT DA CAIXA ESCOLHIDA
        BOXs = self.getListBox(box)

        if len(BOXs) == 0:
            return 0

        else:
            #RETORNA O NOVO ID
            return int(BOXs[-1][0]) + 1

    def getLastID(self, m, y):
        
        #PEGA A LISTA DE GASTOS
        gastos = self.getListaGastosMes(m, y)

        #VERIFICA SE É NULA
        if len(gastos) == 0:
            return 0

        else:
            #RETORNA O NOVO ID
            return int(gastos[-1][0]) + 1 
    
    def getLastIdInvestments(self):
        
        inves = self.getInvestments()

        #VERIFICA SE É NULA
        if len(inves) == 0:
            return 0

        else:
            #RETORNA O NOVO ID
            return int(inves[-1][0]) + 1 

    def getNameMonth(self, m):
        #TRANSFORMA MES DE NUMERO PARA O NOME
        return self.months[m-1]

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

    def getTypeGastos(self, m, y):
        
        listSumGastos = []

        for i in self.spendings:

            #EXIBIR TODOS OS DADOS DE UMA TABELA MES, PELA DATA ESPECIFICA
            show = f"SELECT valor FROM {self.getNameMonth(m)} WHERE ano = '{y}' AND Item LIKE '%{i}%'"

            self.cur.execute(show)
            valores = self.cur.fetchall()

            #SOMA E ADICIONA NA LISTA DE GASTOS POR TIPO

            listSumGastos.append(sum([v[0]*-1 for v in valores]))

        return tuple(listSumGastos)

    # ----------------------------------- SETOR DE EXCLUSÃO DE TUPLAS -----------------------------------
    def dropDespesa(self, m, ind):

        #DELETAR DESPESA
        command = f'DELETE FROM {self.getNameMonth(m)} WHERE id = {ind}'

        self.cur.execute(command)
        self.conection.commit()

        #LOG
        self.insertLog(self.currentData, F'DROP SPENDING IN THE MONTH {m}')

    def dropSpending(self, m, id):
        #EXCLUIR GASTO
        command = F'DELETE FROM {self.getNameMonth(m)} WHERE id = {id}'

        self.cur.execute(command)
        self.conection.commit()

        #LOG
        self.insertLog(self.currentData, F'DROP SPENDING')

    def dropRevenue(self, m, id):
        print('ok')
        #EXCLUIR RECEITA
        command = F'DELETE FROM BOXT WHERE id = {id} AND mes = "{m}"'

        self.cur.execute(command)
        self.conection.commit()

        #LOG
        self.insertLog(self.currentData, F'DROP Revenue')

    # ----------------------------------- SETOR DE UPDATE DE DADOS -----------------------------------
    def updateStatusSpending(self, m, id):

        #EXIBIR TODOS OS DADOS DE UMA TABELA MES, PELA DATA ESPECIFICA  
        show = f"SELECT status FROM {self.getNameMonth(m)} WHERE ID = '{id}'"
        
        self.cur.execute(show)
        item = self.cur.fetchall()

        status = 'PG'

        #CASO ENCONTRE ALGUM ID
        if len(item) != 0:
            
            #FAZ UM SWAP
            if item[0][0] == 'PG':
                status = '--'

        show = F'UPDATE {self.getNameMonth(m)} SET status = "{status}" WHERE id= "{id}"'
        self.cur.execute(show)

        #CONSOLIDAR BASE DE DADOS
        self.conection.commit()

        #LOG
        self.insertLog(self.currentData, F'UPDATE STATUS IN SPENDINGS')
    
    def updateNameSpending(self, m, id, Item):

        #ATUALIZA O NOME DO GASTO
        show = F'UPDATE {self.getNameMonth(m)} SET Item = "{Item}" WHERE id= "{id}"'
        self.cur.execute(show)

        #CONSOLIDAR BASE DE DADOS
        self.conection.commit()

        #LOG
        self.insertLog(self.currentData, F'UPDATE NAME IN SPENDINGS')

    def updateValorSpending(self, m, id, valor):

        #ATUALIZA O NOME DO GASTO
        show = F'UPDATE {self.getNameMonth(m)} SET valor = {valor} WHERE id= "{id}"'
        self.cur.execute(show)

        #CONSOLIDAR BASE DE DADOS
        self.conection.commit()

        #LOG
        self.insertLog(self.currentData, F'UPDATE VALOR IN SPENDINGS')
    
    def updateNomeRevenue(self, m, id, Item):

        #ATUALIZA O NOME DA RECEITA
        show = F'UPDATE BOXT SET Item = "{Item}" WHERE ID= {id} AND mes="{m}"'
        self.cur.execute(show)

        #CONSOLIDAR BASE DE DADOS
        self.conection.commit()

    def updateValorRevenue(self, m, id, valor):

        #ATUALIZA O NOME DA RECEITA
        show = F'UPDATE BOXT SET valor = {valor} WHERE ID= {id} AND mes="{m}"'
        self.cur.execute(show)

        #CONSOLIDAR BASE DE DADOS
        self.conection.commit()
    
    def updateStatusRevenue(self, m, id):

        #EXIBIR TODOS OS DADOS DE UMA TABELA MES, PELA DATA ESPECIFICA  
        show = f"SELECT status FROM BOXT WHERE ID = '{id}' AND mes='{m}'"
        
        self.cur.execute(show)
        item = self.cur.fetchall()

        status = 'PG'

        #CASO ENCONTRE ALGUM ID
        if len(item) != 0:
            
            #FAZ UM SWAP
            if item[0][0] == 'PG':
                status = '--'

        show = F'UPDATE BOXT SET status= "{status}" WHERE id= "{id}"'
        self.cur.execute(show)

        #CONSOLIDAR BASE DE DADOS
        self.conection.commit()

    # ----------------------------------- SETOR DE LIMPEZA DES TABELAS MESES -----------------------------------
    def resetDataBase(self):
        
        for m in range(13):
            
            #EXIBIR TODOS OS DADOS DE UMA TABELA MES, PELA DATA ESPECIFICA
            show = f"SELECT ID FROM {self.getNameMonth(m)}"

            self.cur.execute(show)
            valores = self.cur.fetchall()
            
            #LOG
            self.insertLog(self.currentData, F'FORMAT DATA BASE')

            for i in valores:
                self.dropDespesa(m, i[0])

    # ----------------------------------- SETOR DE CRIAÇÃO DE RELATORIOS -----------------------------------
    def createCSV(self, m, y):

        with open(F'Relatorio_Mensal_{m}-{y}.csv', 'w', newline='') as file:

            #CRIAR O OBJETO
            writer = csv.writer(file)
            
            #CRIAR TUPLA DE INFORMAÇÕES
            writer.writerow(["ID", "Mes", "Ano", "Item", "Valor", "Status"])

            #VARRER LISTA DE GASTOS
            lGastos = self.getListaGastosMes(m, y)

            for i in lGastos:
                writer.writerow([i[0], self.getNameMonth(m), i[1], i[2], i[3], i[4]])       

            #VALOR TOTAL DO MÊS
            total = self.getGastosMes(m, y)

            #VARRER LISTA DE GASTOS
            boxT = self.getListBoxTCurrent(m, y)

            for t in boxT:

                #LISTA DE RECEITAS DO MÊS
                writer.writerow([t[0], self.getNameMonth(m), t[2], t[3], t[4], t[5]])

            totalBoxT = self.getSumBoxT(m, y)

            valorRestante = totalBoxT + total

            #PULA UMA LINHA
            writer.writerow(['', '', '', 'SALDO TOTAL: ', valorRestante, ''])

            #LOG
            self.insertLog(self.currentData, F'CREATE MONTHLY REPORT {m}/{y}')

a = bd()
#a.insertInvestment('05/11/2020', 'ONEF11', 'FII', 'PROV RENDIMENTOS', 0.64)
#a.insertInvestment('05/11/2020', 'TESOURO PRE 2026', 'REND. FIXA', 'COMPRA', 97)
#a.insertInvestment('06/11/2020', 'VINO11', 'FII', 'COMPRA', 60.20)
#a.insertInvestment('09/11/2020', 'ARCT11', 'FII', 'COMPRA', 1119.40)
#a.insertInvestment('09/11/2020', 'BARI11', 'FII', 'COMPRA', 106.33)
#print(a.getInvestments())
#a.insertInvestment('13/11/2020', '', '', '', 145)
#a.createTableInvestments()
#print(a.getTypeGastos(11, 2020))
#a.updateStatusRevenue(11, 0)
#a.updateNomeRevenue(11, 0, 'ABCS')
#a.updateValorRevenue(11, 0, 280)
#a.insertBoxT(11, 2020, 'PARCELA DA MOTO', 300, '--')
#a.createTableLog()
#a.dropRevenue(11, 0)
#a.dropSpending(11, 0)
#a.updateValorSpending(11, 0, -150)
#a.updateNameSpending(11, 0, 'VISEIRA MOTO')
#print(a.getListBoxTCurrent(11, 2020))
#a.insertBoxT(11, 2020, 'PROJETO', 250, '--')
#a.insertBoxT(11, 2020, 'PROJETO EXT.', 250, '--')
#a.insertBox('F', '10/11/2020', 'POUP.', 12000)
#a.insertBox('S', '10/11/2020', 'POUP.', 12000)
#print(a.getSumBox('T'))
#a.createTablesBoxT()
#for i in ['E', 'S', 'F']:
#    a.createTablesBoxs(i)
#a.createCSV(11, 2020)
#a.updateStatus(11, 1)
#for i in a.months:
#    a.createTablesMonths(i)
#a.resetDataBase()