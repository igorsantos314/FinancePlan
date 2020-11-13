from datetime import date
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from dataBase import bd
from plotGraphsFinances import plotGraphs

class months(Frame):

    def __init__(self):

        #OBJETO DE BANCO DE DADOS
        self.bancoDados = bd()

        #OBEJTO DE CRIAÇÃO DE GRAFICOS
        self.graph = plotGraphs()

        #DEFAULT
        self.verdeClaro = 'MediumSpringGreen'
        self.fontStyleUpper = 'Courier 20 bold'
        self.tomato = 'Tomato'
        self.gold= 'PaleGoldenrod'
        self.azulClaro = 'PowderBlue'
        self.fontDefault = 'Courier 12'
        self.fontTad = 'Courier 12 bold'

        #MENU
        self.bgMenu = 'Black'
        self.colorTaps = 'Cyan'
        self.colorBox = 'SpringGreen'
        self.colorInvestments = 'Orange'

        #DATA ATUAL
        self.day = date.today().day
        self.month = date.today().month
        self.year = date.today().year

        #MES CORRENTE PARA PESQUISAS
        self.currentMonth = self.month
        self.currentYear = date.today().year

        #CALL WINDOW MAIN
        self.windowSpending()

    def windowSpending(self):

        self.windowMain = Tk()
        self.windowMain.geometry('995x500+10+10')
        self.windowMain.resizable(False, False)
        self.windowMain.title('FINANCE')
        self.windowMain['bg'] = 'black'

        #BARRA DE FUNÇÕES
        menubar = Menu(self.windowMain, bg=self.bgMenu, fg='White', font=self.fontDefault)
        myMenu = Menu(menubar, tearoff=0)

        #MENU FILE
        fileMenuFile = Menu(myMenu, bg=self.bgMenu, fg='White', font=self.fontDefault)
        fileMenuFile.add_command(label='New Spending', command=self.insertDespesa)
        fileMenuFile.add_command(label='New Revenue', command=self.insertRevenue)

        fileMenuFile.add_separator()
        fileMenuFile.add_command(label='View Log', command='')
        fileMenuFile.add_command(label='Monthly Report', command=self.createMonthlyReport)
        fileMenuFile.add_command(label='Graph Spendings Type', command=self.plotGraphSpendingMonth)

        menubar.add_cascade(label="File", menu=fileMenuFile)

        #FILE MENU DE TORNEIRAS
        fileMenuTap = Menu(myMenu, bg=self.bgMenu, fg=self.colorTaps, font=self.fontDefault)
        fileMenuTap.add_command(label='Edit Name', command=self.updateNameSpending)
        fileMenuTap.add_command(label='Edit Value', command='')
        fileMenuTap.add_command(label='Update Status', command=self.updateStatus)

        fileMenuTap.add_separator()

        fileMenuTap.add_command(label='Del Tap', command=self.deleteSpending)
        menubar.add_cascade(label="Taps", menu=fileMenuTap)

        #FILE MENU DE CAIXAS
        fileMenuBox = Menu(myMenu, bg=self.bgMenu, fg=self.colorBox, font=self.fontDefault)
        fileMenuBox.add_command(label='Cash Deposit BOX E', command='')
        fileMenuBox.add_command(label='Cash Deposit BOX S', command='')
        fileMenuBox.add_command(label='Cash Deposit BOX F', command='')

        fileMenuBox.add_separator()
        fileMenuBox.add_command(label='Update Status', command=self.updateStatusBox)
        fileMenuBox.add_separator()

        fileMenuBox.add_command(label='Del Revenue', command=self.deleteRevenue)

        menubar.add_cascade(label="Boxes", menu=fileMenuBox)

        #FILE MENU DE INVESTIMENTOS
        fileInvestments = Menu(myMenu, bg=self.bgMenu, fg=self.colorInvestments, font=self.fontDefault)
        fileInvestments.add_command(label='New Investiment', command='')
        fileInvestments.add_command(label='View Investments', command=self.viewInvestments)
        fileInvestments.add_command(label='Add Dividends', command='')

        fileInvestments.add_separator()
        fileInvestments.add_command(label='Close Table', command=self.closeTableInvestments)
        fileInvestments.add_separator()

        fileInvestments.add_command(label='Update Investiment', command=self.updateStatusBox)
        fileInvestments.add_separator()

        fileInvestments.add_command(label='Del Investiment', command=self.deleteRevenue)

        menubar.add_cascade(label="Investments", menu=fileInvestments)

        #SETAR TITULO DA JANELA PRINCIPAL
        self.lblTitle = Label(text='', font=self.fontStyleUpper, bg='black', fg='white')
        self.lblTitle.pack(pady=30)
        
        self.setTitleWindowMain()
    
        #CREATE LISTBOX TORNEIRAS
        self.setListBoxSpending()

        #CREATE LISTBOX DA CAIXA T
        self.setListBoxT()

        #CREATE LISTBOX DAS CAIXAS E S F
        #self.setListBoxESF()

        #INICIALIZA AS TABELAS
        self.refreshTables()

        #TECLAS DE FUNCOES
        self.windowMain.bind("<F1>", self.keyPressed)
        self.windowMain.bind("<F2>", self.keyPressed)
        self.windowMain.bind("<F3>", self.keyPressed)
        self.windowMain.bind("<F5>", self.keyPressed)
        self.windowMain.bind("<F6>", self.keyPressed)
        self.windowMain.bind("<F8>", self.keyPressed)

        #configurar file menu
        self.windowMain.config(menu=menubar)

        self.windowMain.mainloop()

    # ----------------------- SETOR DE CAPTAÇÃO DE TEVLAS DE ATALHO -----------------------
    def keyPressed(self, event):
        l = event.keysym

        if l == 'F2':
            #ADICIONAR NOVA DESPESA
            self.insertDespesa()

        elif l == 'F5':
            #ATUALIZA A LISTA DE GASTOS
            self.insertSpendingListBox()

            #ATUALIZA LISTA DA RECEITA
            self.insertRevenueListBox()

        elif l == 'F6':
            #VOLTA UM MES
            self.prevMonth()

        elif l == 'F8':
            #AVANÇA UM MES
            self.nextMonth()
    
    # ----------------------- SETOR DE DEFINIÇÃO DE TITULO -----------------------
    def setTitleWindowMain(self):
        #DEFINE O TITULO
        self.lblTitle['text'] = f'FINANCES OF {self.bancoDados.getNameMonth(self.currentMonth)} OF {self.currentYear}'

    # ----------------------- SETOR DE MODIFICAÇÃO DE MES -----------------------
    def nextMonth(self):
            
        #VERIFICA SE ESTA EM DEZEMBRO E AVANÇA UM ANO
        if self.currentMonth == 12:
            self.currentMonth = 1
            self.currentYear += 1
        
        else:
            self.currentMonth += 1

        #ATUALIZA OS VALORES E O TITULO DA JANELA
        self.setTitleWindowMain()

        #ATUALIZA AS TABELAS
        self.refreshTables()

    def prevMonth(self):

        #VERIFICA SE ESTA EM JANEIRO E VOLTA UM ANO ATRAS
        if self.currentMonth == 1:
            self.currentMonth = 12
            self.currentYear -= 1
        
        else:
            self.currentMonth -= 1

        #ATUALIZA OS VALORES E O TITULO DA JANELA
        self.setTitleWindowMain()

        #ATUALIZA AS TABELAS
        self.refreshTables()

    def refreshTables(self):
        #ATUALIZA A LISTA DE GASTOS
        self.insertSpendingListBox()

        #ATUALIZA LISTA DA RECEITA
        self.insertRevenueListBox()
    
    # ----------------------- SETOR DE CRIAÇÃO DOS LISTBOXs -----------------------
    def setListBoxSpending(self):
        #LABEL DE GASTOS
        lblGastos = Label(text='WATER TAP', font=self.fontStyleUpper, bg='black', fg=self.colorTaps)
        lblGastos.place(x=10, y=80)
        #lblGastos.grid(column=0, row=1, pady=5, padx=10)

        self.listboxtTaps = Listbox(self.windowMain, height=20, width=50, font= self.fontDefault, bg='black', fg='cyan')
        self.listboxtTaps.pack(side=LEFT, padx=10)
        #self.listboxtTaps.grid(column=0, row=2, pady=5, padx=10)

    def setListBoxT(self):
        #LABEL DE RECEITA DO MES
        lblReceita = Label(text='BOX T', font=self.fontStyleUpper, bg='black', fg=self.colorBox)
        lblReceita.place(x=532, y=80)

        self.listboxBox = Listbox(self.windowMain, height=20, width=45, font= self.fontDefault, bg='black', fg=self.colorBox)
        self.listboxBox.pack(side=RIGHT, padx=10)
        #self.listboxBox.grid(column=1, row=2, pady=5, padx=5)

    # ----------------------- SETOR DE INSERÇÃO NO LITBOX -----------------------
    def insertRevenueListBox(self, m=None, y=None):

        #INCIALIZADOR PADRÃO
        if m is None:
            m = self.currentMonth
            y = self.currentYear

        #LIMPAR LISTBOX
        self.listboxBox.delete(0,'end')

        #INSERIR CABEÇALHO
        self.listboxBox.insert("end", 'CODE    NAME              VALUE     STATUS')
        self.listboxBox.insert("end", '-------------------------------------------')

        #PEGAR LISTA DE GASTOS DO MÊS CORRENTE
        listBotT = self.bancoDados.getListBoxTCurrent(m, y)

        for i in listBotT:

            #FORMATAÇÃO DOS DADOS
            id = "{}".format(i[0])
            id = "{}{}".format(i[0], " " * (8 - len(id)))

            nome = "{}{}".format(i[3], " " * (18 - len(i[3])))

            valor = "{}".format(i[4])
            valor = "R${}{}".format(valor, " " * (10 - len(valor)))

            statusPag = "{}{}".format(i[5], " " * (12 - len(i[5])))

            #INSERIR A TUPLA NO FINAL DO LISTBOX
            self.listboxBox.insert("end", F'{id}{nome}{valor}{statusPag}')

        #SOMA DAS RECEITAS DO MES
        total = self.bancoDados.getSumBoxT(m, y)

        #INSERIR DESPESAS NO LISTBOX
        self.listboxBox.insert("end", '-------------------------------------------')
        space = ' ' * 10

        self.listboxBox.insert("end", F'        TOTAL: {space} R${total}')

    def insertSpendingListBox(self, m=None, y=None):

        #INCIALIZADOR PADRÃO
        if m is None:
            m = self.currentMonth
            y = self.currentYear

        #LIMPAR LISTBOX
        self.listboxtTaps.delete(0,'end')

        #INSERIR CABEÇALHO
        self.listboxtTaps.insert("end", 'CODE    NAME                     VALUE     STATUS')
        self.listboxtTaps.insert("end", '---------------------------------------------------')

        #PEGAR LISTA DE GASTOS DO MÊS CORRENTE
        listSpending = self.bancoDados.getListaGastosMes(m, y)

        for i in listSpending:

            #tratamento de dados
            id = "{}".format(i[0])
            id = "{}{}".format(i[0], " " * (8 - len(id)))

            nome = "{}{}".format(i[2], " " * (25 - len(i[2])))

            valor = "{}".format(i[3])
            valor = "R${}{}".format(valor, " " * (10 - len(valor)))

            statusPag = i[4]

            self.listboxtTaps.insert("end", F'{id}{nome}{valor}{statusPag}')

        #SOMA DAS DESPESAS
        total = self.bancoDados.getGastosMes(m, y)

        #INSERIR DESPESAS NO LISTBOX
        self.listboxtTaps.insert("end", '---------------------------------------------------')
        space = ' ' * 17

        self.listboxtTaps.insert("end", F'        TOTAL: {space} R${total}')

    def viewInvestments(self):

        self.listboxInvestments = Listbox(self.windowMain, height=27, width=99, font= self.fontDefault, bg='black', fg=self.colorInvestments)
        self.listboxInvestments.place(x=0, y=0)

        #INSERIR CABEÇALHO
        self.listboxInvestments.insert("end", 'CODE    DATE         NAME ACTIVE         TYPE ACTIVE           TRANSACTION TYPE       VALUE')
        self.listboxInvestments.insert("end", '-------------------------------------------------------------------------------------------------')

        #PEGAR LISTA DE GASTOS DO MÊS CORRENTE
        listInvestments = self.bancoDados.getInvestments()

        for i in listInvestments:

            #FORMATAÇÃO DE STRING
            id = "{}".format(i[0])
            id = "{}{}".format(i[0], " " * (8 - len(id)))

            data = "{}{}".format(i[1], " " * (13 - len(i[1])))

            nomeAtivo = "{}{}".format(i[2], " " * (20 - len(i[2])))
            tipoAtivo = "{}{}".format(i[3], " " * (22 - len(i[3])))
            tipoTransacao = "{}{}".format(i[4], " " * (23 - len(i[4])))

            valor = F'R${i[5]}'

            self.listboxInvestments.insert("end", F'{id}{data}{nomeAtivo}{tipoAtivo}{tipoTransacao}{valor}')

    def closeTableInvestments(self):

        #DESTROY LIST BOX DE INVESTIMENTOS CASO ESTEJA ABERTO
        try:
            self.listboxInvestments.destroy()

        except:
            pass

    # ----------------------- SETOR DE UPDATE DE STATUS -----------------------
    def updateStatus(self):

        try:
            indice = self.listboxtTaps.curselection()[0]
            id = int(self.listboxtTaps.get(indice).split(" ")[0])
            
            #ATUALIZAR O STATUS        
            self.bancoDados.updateStatusSpending(self.currentMonth, id)

            #ATUALIZAR TABELAS
            self.refreshTables()

        except:
            pass

    # ----------------------- SETOR DE UPDATE DE NOME -----------------------
    def updateNameSpending(self):

        #CRIAR FUNDO PRETO
        self.createBackGround()

        lblTitle = Label(text='Update Name Spending', font=self.fontStyleUpper, bg=self.bgMenu, fg=self.colorTaps)
        lblTitle.place(x=280, y=100)

        #DESPESA
        lblDespesa = Label(text='Despesa:', font= self.fontDefault, bg=self.bgMenu, fg=self.colorTaps)
        lblDespesa.place(x=280, y=140)

        comboDespesa = ttk.Combobox(width=12, font= self.fontDefault) 

        comboDespesa['values'] = tuple(['ALIMENTACAO', 'COMBUSTIVEL', 'CARTAO -', 'SAUDE', 'COMBUSTIVEL', 'TRANSPORTE', 'MTL', 'OUTROS'])
        comboDespesa.current(0)
        comboDespesa.place(x=280, y=160)

        def save():
            pass

        #BOTAO DE SALVAMENTO
        btSave = Button(text='SAVE', bg=self.bgMenu, fg='MediumSpringGreen', command=save)
        btSave.place(x=585, y=400)

        #BOTAO PARA DESTRUIR TODOS OS ITENS
        btDestroy = Button(text='CLOSE', bg=self.bgMenu, fg='Tomato', command=lambda:destroyItens())
        btDestroy.place(x=500, y=400)

        #DESTRUI ITENS
        def destroyItens():
            
            lblTitle.destroy()
            lblDespesa.destroy()
            comboDespesa.destroy()

            btSave.destroy()
            btDestroy.destroy()

            self.backGround.destroy()

    def updateStatusBox(self):

        try:
            indice = self.listboxBox.curselection()[0]
            id = int(self.listboxBox.get(indice).split(" ")[0])
            
            #ATUALIZAR O STATUS        
            self.bancoDados.updateStatusRevenue(self.currentMonth, id)

            #ATUALIZAR TABELAS
            self.refreshTables()

        except:
            pass

    # ----------------------- SETOR DE CRIAÇÃO DE WINDOW ACLOPLADA  -----------------------
    def createBackGround(self):

        self.backGround = Label(bg=self.bgMenu, width=50, height=20)
        self.backGround.place(x=270, y=100)

    # ----------------------- SETOR DE INSERÇAO DE RECEIVES AND SPENDINGS -----------------------
    def insertDespesa(self):

        #CRIAR FUNDO PRETO
        self.createBackGround()

        lblTitle = Label(text='New Spending', font= self.fontStyleUpper, bg=self.bgMenu, fg=self.colorTaps)
        lblTitle.place(x=280, y=100)

        #Mes
        lblMes = Label(text='Mês:', font= self.fontDefault, bg=self.bgMenu, fg=self.colorTaps)
        lblMes.place(x=280, y=140)

        comboMes = ttk.Combobox(width= 10, font= self.fontDefault) 

        comboMes['values'] = tuple([i for i in range(1, 12)])
        comboMes.current(self.month-1)
        comboMes.place(x=280, y=160)

        #Ano
        lblAno = Label(text='Ano:', font= self.fontDefault, bg=self.bgMenu, fg=self.colorTaps)
        lblAno.place(x=430, y=140)

        comboAno = ttk.Combobox(width=12, font= self.fontDefault) 

        comboAno['values'] = tuple(['{}'.format(i) for i in range(2020, 2051)])
        comboAno.current(0)
        comboAno.place(x=430, y=160)

        #DESPESA
        lblDespesa = Label(text='Despesa:', font= self.fontDefault, bg=self.bgMenu, fg=self.colorTaps)
        lblDespesa.place(x=280, y=200)

        comboDespesa = ttk.Combobox(width=12, font= self.fontDefault) 

        comboDespesa['values'] = tuple(['ALIMENTACAO', 'COMBUSTIVEL', 'CARTAO -', 'SAUDE', 'COMBUSTIVEL', 'TRANSPORTE', 'MTL', 'OUTROS'])
        comboDespesa.current(0)
        comboDespesa.place(x=280, y=220)

        #VALOR
        lblValor = Label(text='Valor:', font= self.fontDefault, bg=self.bgMenu, fg=self.colorTaps)
        lblValor.place(x=430, y=200)

        etValor = Entry(width=9)
        etValor.place(x=430, y=220)

        #MACRO
        lblMacro = Label(text='Macro:', font= self.fontDefault, bg=self.bgMenu, fg=self.colorTaps)
        lblMacro.place(x=280, y=260)

        comboMacro = ttk.Combobox(width=12, font= self.fontDefault, ) 

        comboMacro['values'] = tuple([i for i in range(1, 24)])
        comboMacro.current(0)
        comboMacro.place(x=280, y=280)

        #SALVAR TODOS OS DADOS
        def save():

            try:
                #QUANTIDAD ED EPARCELAS
                iteracoes = int(comboMacro.get())
                
                #INFORMAÇẼOS DA COMPRA
                mes = int(comboMes.get())
                ano = int(comboAno.get())
                item  = comboDespesa.get().upper()[:20]
                valor = -float(etValor.get())

                #ADICIONAR O MESMO VALOR EM VÁRIOS MESES
                for i in range(iteracoes):
                    
                    #RESETA O MES A ATUALIZA O ANO
                    if mes > 12:
                        mes = 1
                        ano += 1

                    #CASO SEJA PARCELADO
                    if iteracoes > 1:
                        item = F'{comboDespesa.get().upper()} {i+1}/{iteracoes}'

                    #ADICIONAR NA BASE DE DADOS
                    self.bancoDados.insertItem(mes, ano, item, valor, '--')

                    #MODIFICA O MES
                    mes += 1

                #MENSAGEM DE SUCESSO
                messagebox.showinfo('', 'Adicionado Com Sucesso !')

                #ATUALIZA AS TABELAS
                self.refreshTables()

                #RESETA OS CAMPOS DE VALOR E MACRO
                etValor.delete(0, END)

                comboMacro.current(0)

            except:
                messagebox.showerror('', 'Ocorreu um Erro !')

        #BOTAO DE SALVAMENTO
        btSave = Button(text='SAVE', bg='MediumSpringGreen', command=save)
        btSave.place(x=585, y=400)

        #BOTAO PARA DESTRUIR TODOS OS ITENS
        btDestroy = Button(text='CLOSE', bg='Tomato', command=lambda:destroyItens())
        btDestroy.place(x=500, y=400)

        #DESTRUI ITENS
        def destroyItens():
            
            lblTitle.destroy()

            lblMes.destroy()
            lblAno.destroy()
            lblDespesa.destroy()
            lblValor.destroy()
            lblMacro.destroy()
            
            comboMes.destroy()
            comboAno.destroy()
            comboDespesa.destroy()
            comboMacro.destroy()

            etValor.destroy()

            btSave.destroy()
            btDestroy.destroy()

            self.backGround.destroy()

    def insertRevenue(self):

        #CRIAR FUNDO PRETO
        self.createBackGround()

        lblTitle = Label(text='New Revenue', font= self.fontStyleUpper, bg=self.bgMenu, fg=self.colorBox)
        lblTitle.place(x=280, y=100)

        #Mes
        lblMes = Label(text='Mês:', font= self.fontDefault, bg=self.bgMenu, fg=self.colorBox)
        lblMes.place(x=280, y=140)

        comboMes = ttk.Combobox(width= 15, font= self.fontDefault) 

        comboMes['values'] = tuple([i for i in range(1, 12)])
        comboMes.current(self.month-1)
        comboMes.place(x=280, y=160)

        #Ano
        lblAno = Label(text='Ano:', font= self.fontDefault, bg=self.bgMenu, fg=self.colorBox)
        lblAno.place(x=430, y=140)

        comboAno = ttk.Combobox(width=12, font= self.fontDefault) 

        comboAno['values'] = tuple(['{}'.format(i) for i in range(2020, 2051)])
        comboAno.current(0)
        comboAno.place(x=430, y=160)

        #RECEIVE
        lblRevenue = Label(text='Origem:', font= self.fontDefault, bg=self.bgMenu, fg=self.colorBox)
        lblRevenue.place(x=280, y=200)

        comboRevenue = ttk.Combobox(width=12, font= self.fontDefault) 

        comboRevenue['values'] = tuple(['TRABALHO', 'PROEJETO', 'DESENV.', 'ESCOLA', 'INVESTIMENTOS', 'OUTROS'])
        comboRevenue.current(0)
        comboRevenue.place(x=280, y=220)

        #VALOR
        lblValor = Label(text='Valor:', font= self.fontDefault, bg=self.bgMenu, fg=self.colorBox)
        lblValor.place(x=430, y=200)

        etValor = Entry(width=9)
        etValor.place(x=430, y=220)

        #MACRO
        lblMacro = Label(text='Macro:', font= self.fontDefault, bg=self.bgMenu, fg=self.colorBox)
        lblMacro.place(x=280, y=260)

        comboMacro = ttk.Combobox(width=12, font= self.fontDefault, ) 

        comboMacro['values'] = tuple([i for i in range(1, 24)])
        comboMacro.current(0)
        comboMacro.place(x=280, y=280)

        #SALVAR TODOS OS DADOS
        def save():

            try:
                #QUANTIDAD ED EPARCELAS
                iteracoes = int(comboMacro.get())
                
                #INFORMAÇẼOS DA COMPRA
                mes = int(comboMes.get())
                ano = int(comboAno.get())
                item  = comboRevenue.get().upper()[:20]
                valor = +float(etValor.get())

                #ADICIONAR O MESMO VALOR EM VÁRIOS MESES
                for i in range(iteracoes):
                    
                    #RESETA O MES A ATUALIZA O ANO
                    if mes > 12:
                        mes = 1
                        ano += 1

                    #CASO SEJA PARCELADO
                    if iteracoes > 1:
                        item = F'{comboRevenue.get().upper()} {i+1}/{iteracoes}'

                    #ADICIONAR NA BASE DE DADOS
                    self.bancoDados.insertBoxT(mes, ano, item, valor, '--')

                    #MODIFICA O MES
                    mes += 1

                #MENSAGEM DE SUCESSO
                messagebox.showinfo('', 'Adicionado Com Sucesso !')

                #ATUALIZA AS TABELAS
                self.refreshTables()

                #RESETA OS CAMPOS DE VALOR E MACRO
                etValor.delete(0, END)

                comboMacro.current(0)

            except:
                messagebox.showerror('', 'Ocorreu um Erro !')

        #BOTAO DE SALVAMENTO
        btSave = Button(text='SAVE', bg=self.bgMenu, fg='MediumSpringGreen', command=save)
        btSave.place(x=585, y=400)

        #BOTAO PARA DESTRUIR TODOS OS ITENS
        btDestroy = Button(text='CLOSE', bg=self.bgMenu, fg='Tomato', command=lambda:destroyItens())
        btDestroy.place(x=500, y=400)

        #DESTRUI ITENS
        def destroyItens():
            
            lblTitle.destroy()

            lblMes.destroy()
            lblAno.destroy()
            lblRevenue.destroy()
            lblValor.destroy()
            lblMacro.destroy()
            
            comboMes.destroy()
            comboAno.destroy()
            comboRevenue.destroy()
            comboMacro.destroy()

            etValor.destroy()

            btSave.destroy()
            btDestroy.destroy()

            self.backGround.destroy()

    # ----------------------- SETOR DE EXCLUSÃO -----------------------
    def deleteSpending(self):
        
        try:
            #PEGA O ID DO INDICE SELECIONADO NO LISTBOX
            indice = self.listboxtTaps.curselection()[0]
            id = int(self.listboxtTaps.get(indice).split(" ")[0])
            
            if messagebox.askquestion('', F'Delete Spending ID: {id} ?') == 'yes':
                
                #DELETA O ITEM SELECIONADO    
                self.bancoDados.dropSpending(self.currentMonth, id)

                #ATUALIZAR LISTBOX
                self.insertSpendingListBox()

        except:
            pass

    def deleteRevenue(self):
        
        #PEGA O ID DO INDICE SELECIONADO NO LISTBOX
        indice = self.listboxBox.curselection()[0]
        id = int(self.listboxBox.get(indice).split(" ")[0])
        
        if messagebox.askquestion('', F'Delete Revenue ID: {id} ?') == 'yes':
            
            #DELETA O ITEM SELECIONADO    
            self.bancoDados.dropRevenue(self.currentMonth, id)

            #ATUALIZAR LISTBOX
            self.insertRevenueListBox()                
    
    # ----------------------- SETOR DE CRIAÇÃO DE RALATORIOS -----------------------
    def createMonthlyReport(self):

        try:
            #CRIAR CSV
            self.bancoDados.createCSV(self.currentMonth, self.currentYear)

            #MENSAGEM DE SUCESSO
            messagebox.showinfo('SUCESSO', f'RELATÓRIO MENSAL DE {self.currentMonth}/{self.currentYear} CRIADO!')

        except:
            messagebox.showerror('', 'OCORREU UM ERRO :(')

    def plotGraphSpendingMonth(self):

        #SOMA POR TIPO DE GASTO
        spendings = self.bancoDados.getTypeGastos(self.currentMonth, self.currentYear)

        #INDICES DA COLUNA Y
        index = self.bancoDados.spendings

        #GERAR GRAFICO
        self.graph.generateGraph(spendings, index, 'SPENDING MONTH', 'VALOR EM R$', 'SPENDINGS')

if __name__ == "__main__":
    m = months()