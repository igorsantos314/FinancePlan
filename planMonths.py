from datetime import date
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from dataBase import bd
from plotGraphsFinances import plotGraphs
from backup import backup

class months(Frame):

    def __init__(self):

        #OBJETO DE BANCO DE DADOS
        self.bancoDados = bd()
        self.backup = backup()

        #OBEJTO DE CRIAÇÃO DE GRAFICOS
        self.graph = plotGraphs()

        #DEFAULT
        self.verdeClaro = 'MediumSpringGreen'
        self.fontStyleUpper = 'Courier 20 bold'
        self.tomato = 'Tomato'
        self.gold= 'PaleGoldenrod'
        self.azulClaro = 'PowderBlue'
        self.fontDefault = 'Courier 12'
        self.fontTad = 'Coureir 12 bold'

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
        self.windowMain.geometry('1020x500+10+10')
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
        fileMenuFile.add_command(label='Monthly Report', command=self.createMonthlyReport)
        fileMenuFile.add_command(label='Graph Spendings Type', command=self.plotGraphSpendingMonth)
        fileMenuFile.add_command(label='Backup', command=self.generateBackup)

        menubar.add_cascade(label="File", menu=fileMenuFile)

        #FILE MENU DE TORNEIRAS
        fileMenuTap = Menu(myMenu, bg=self.bgMenu, fg=self.colorTaps, font=self.fontDefault)
        fileMenuTap.add_command(label='Edit Name', command=  lambda: self.updateNameSpending())
        fileMenuTap.add_command(label='Edit Value', command= lambda: self.updateValueSpending())
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
        fileMenuBox.add_command(label='Edit Name', command=  lambda: self.updateNameBox())
        fileMenuBox.add_command(label='Edit Value', command= lambda: self.updateValueRevenue())
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
        self.lblTitle.pack()
        
        self.setTitleWindowMain()
        
        #CREATE TREE VIEW DE GASTOS
        self.setTreeViewSpendings()

        #CREATE TREE VIEW DE RECEITAS
        self.setTreeViewRevenue()
        
        #CREATE LABEL COM O NOME DE TOTAL BRANCO
        lblTotalSpendings = Label(text='TOTAL:', font=self.fontStyleUpper, fg='white', bg='black')
        lblTotalSpendings.place(x=10, y=430)

        lblTotalRevenue = Label(text='TOTAL:', font=self.fontStyleUpper, fg='white', bg='black')
        lblTotalRevenue.place(x=500, y=430)

        #INICIALIZA AS TABELAS
        self.insertSpendingsTreeView()
        self.insertRevenueTreeView()

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

    # ----------------------- SETOR DE CAPTAÇÃO DE TECLAS DE ATALHO -----------------------
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
        #LIMPAR TABELAS
        self.clearAllSpendings()
        self.clearAllRevenue()

        #ATUALIZA A LISTA DE GASTOS
        self.insertSpendingsTreeView()

        #ATUALIZA LISTA DA RECEITA
        self.insertRevenueTreeView()
    
    # ----------------------- SETOR DE CRIAÇÃO DE TREEVIEW -----------------------
    def setTreeViewSpendings(self):

        lblSpendings = Label(text='WATER TAP', font=self.fontStyleUpper, fg=self.colorTaps, bg='black')
        lblSpendings.place(x=10, y=50)

        # Using treeview widget 
        self.treeViewSpendings = ttk.Treeview(self.windowMain, selectmode ='browse', height=15) 
        self.treeViewSpendings.place(x=10, y=100)

        # Constructing vertical scrollbar 
        # with treeview 
        verscrlbar = ttk.Scrollbar(self.windowMain, orient ="vertical", command = self.treeViewSpendings.yview) 
        verscrlbar.pack(side ='right', fill ='x') 

        # Configuring treeview 
        self.treeViewSpendings.configure(xscrollcommand = verscrlbar.set) 

        # Defining number of columns 
        self.treeViewSpendings["columns"] = ("1", "2", "3", "4") 

        # Defining heading 
        self.treeViewSpendings['show'] = 'headings'

        self.treeViewSpendings.column("1", width = 40, anchor ='c') 
        self.treeViewSpendings.column("2", width = 200, anchor ='se') 
        self.treeViewSpendings.column("3", width = 120, anchor ='se') 
        self.treeViewSpendings.column("4", width = 120, anchor ='se')

        self.treeViewSpendings.heading("1", text ="Id") 
        self.treeViewSpendings.heading("2", text ="Name") 
        self.treeViewSpendings.heading("3", text ="Value")
        self.treeViewSpendings.heading("4", text ="Status")

        #LABEL DE VALOR TOTAL DA RECEITA
        self.totalSpendings= Label(text='', font=self.fontStyleUpper, fg=self.colorTaps, bg='black' )
        self.totalSpendings.place(x=80, y=430)

    def setTreeViewRevenue(self):
    
        lblRevenue = Label(text='BOX T', font=self.fontStyleUpper, fg=self.colorBox, bg='black')
        lblRevenue.place(x=500, y=50)

        # Using treeview widget 
        self.treeViewRevenue = ttk.Treeview(self.windowMain, selectmode ='browse', height=15) 
        self.treeViewRevenue.place(x=500, y=100)

        # Constructing vertical scrollbar 
        # with treeview 
        verscrlbar = ttk.Scrollbar(self.windowMain, orient ="vertical", command = self.treeViewSpendings.yview) 
        verscrlbar.pack(side ='right', fill ='x') 

        # Configuring treeview 
        self.treeViewRevenue.configure(xscrollcommand = verscrlbar.set) 

        # Defining number of columns 
        self.treeViewRevenue["columns"] = ("1", "2", "3", "4") 

        # Defining heading 
        self.treeViewRevenue['show'] = 'headings'

        self.treeViewRevenue.column("1", width = 40, anchor ='c') 
        self.treeViewRevenue.column("2", width = 200, anchor ='se') 
        self.treeViewRevenue.column("3", width = 120, anchor ='se') 
        self.treeViewRevenue.column("4", width = 120, anchor ='se')

        self.treeViewRevenue.heading("1", text ="Id") 
        self.treeViewRevenue.heading("2", text ="Name") 
        self.treeViewRevenue.heading("3", text ="Value")
        self.treeViewRevenue.heading("4", text ="Status")

        #LABEL DE VALOR TOTAL DA RECEITA
        self.totalRevenue = Label(text='', font=self.fontStyleUpper, fg=self.colorBox, bg='black' )
        self.totalRevenue.place(x=570, y=430)
    
    # ----------------------- SETOR DE INSERÇÃO DE TREEVIEW -----------------------
    def insertSpendingsTreeView(self, m=None, y=None):
        
        #INCIALIZADOR PADRÃO
        if m is None:
            m = self.currentMonth
            y = self.currentYear

        #LIMPAR TREEVIEW
        self.clearAllSpendings()

        #PEGAR LISTA DE GASTOS DO MÊS CORRENTE
        listSpending = self.bancoDados.getListaGastosMes(m, y)

        for i in listSpending:
            self.treeViewSpendings.insert("", 'end', text ="L1", values =(i[0], i[2], i[3], i[4]))

        #SOMA DOS GASTOS
        total = self.bancoDados.getGastosMes(self.currentMonth, self.currentYear)
        self.totalSpendings['text'] = F'       R$ {total}'
    
    def insertRevenueTreeView(self, m=None, y=None):
    
        #INCIALIZADOR PADRÃO
        if m is None:
            m = self.currentMonth
            y = self.currentYear

        #LIMPAR TREEVIEW
        self.clearAllRevenue()

        #PEGAR LISTA DE GASTOS DO MÊS CORRENTE
        listBoxT = self.bancoDados.getListBoxTCurrent(m, y)

        for i in listBoxT:
            self.treeViewRevenue.insert("", 'end', text ="L1", values =(i[0], i[3], i[4], i[5]))

        #SOMA DAS RECEITAS RECEBIDAS
        total = self.bancoDados.getSumBoxT(self.currentMonth, self.currentYear)
        self.totalRevenue['text'] = F'       R$ {total}'

    # ----------------------- SETOR DE LIMPEZA DE TREEVIEW -----------------------
    def clearAllSpendings(self):

        #PEGA TODOS OS FILHOS
        x = self.treeViewSpendings.get_children()

        #VERIFICA SE NÃO ESTÁ FAZIA
        if x != '()':

            #VARRE A LISTA
            for child in x:

                #DELETA O ITEM CORRESPONDENTE
                self.treeViewSpendings.delete(child)

    def clearAllRevenue(self):
    
        #PEGA TODOS OS FILHOS
        x = self.treeViewRevenue.get_children()

        #VERIFICA SE NÃO ESTÁ FAZIA
        if x != '()':

            #VARRE A LISTA
            for child in x:

                #DELETA O ITEM CORRESPONDENTE
                self.treeViewRevenue.delete(child)

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
            #PEGA O ID
            itemSelecionado = self.treeViewSpendings.selection()[0]
            id = self.treeViewSpendings.item(itemSelecionado, "values")[0]

            #ATUALIZAR O STATUS        
            self.bancoDados.updateStatusSpending(self.currentMonth, id)

            #ATUALIZAR TABELAS
            self.refreshTables()
        
        except:
            pass

    def updateStatusBox(self):
    
        try:
            #PEGA O ID
            itemSelecionado = self.treeViewRevenue.selection()[0]
            id = self.treeViewRevenue.item(itemSelecionado, "values")[0]
            
            #ATUALIZAR O STATUS        
            self.bancoDados.updateStatusRevenue(self.currentMonth, id)

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

        comboDespesa['values'] = self.bancoDados.spendings
        comboDespesa.current(0)
        comboDespesa.place(x=280, y=160)

        def save():
            #PEGA O ID
            itemSelecionado = self.treeViewSpendings.selection()[0]
            id = self.treeViewSpendings.item(itemSelecionado, "values")[0]

            newItem = comboDespesa.get()

            if messagebox.askquestion('Update Name', F'DESEJAR ALTERA NOME ID [{id}]?') == 'yes':
                
                #ATUALIZA O NOME NO BANCO DE DADOS
                self.bancoDados.updateNameSpending(self.currentMonth, id, newItem)
                
                #ATUALIZA AS TABELAS
                self.refreshTables()

                #MENSAGEM DE SUCESSO
                messagebox.showinfo('', 'Atualizado Com Sucesso !')

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

    def updateNameBox(self):
        #CRIAR FUNDO PRETO
        self.createBackGround()

        lblTitle = Label(text='Update Name Revenue', font=self.fontStyleUpper, bg=self.bgMenu, fg=self.colorTaps)
        lblTitle.place(x=280, y=100)

        #TRABALHO
        lblRevenue = Label(text='Revenue:', font= self.fontDefault, bg=self.bgMenu, fg=self.colorTaps)
        lblRevenue.place(x=280, y=140)

        comboRevenue = ttk.Combobox(width=12, font= self.fontDefault) 

        comboRevenue['values'] = self.bancoDados.revenues
        comboRevenue.current(0)
        comboRevenue.place(x=280, y=160)

        def save():
            #PEGA O ID
            itemSelecionado = self.treeViewRevenue.selection()[0]
            id = self.treeViewRevenue.item(itemSelecionado, "values")[0]

            newItem = comboRevenue.get()

            if messagebox.askquestion('Update Name', F'DESEJAR ALTERA NOME ID [{id}]?') == 'yes':
                
                #ATUALIZA O NOME NO BANCO DE DADOS
                self.bancoDados.updateNomeRevenue(self.currentMonth, id, newItem)
                
                #ATUALIZA AS TABELAS
                self.refreshTables()

                #MENSAGEM DE SUCESSO
                messagebox.showinfo('', 'Atualizado Com Sucesso !')

        #BOTAO DE SALVAMENTO
        btSave = Button(text='SAVE', bg=self.bgMenu, fg='MediumSpringGreen', command=save)
        btSave.place(x=585, y=400)

        #BOTAO PARA DESTRUIR TODOS OS ITENS
        btDestroy = Button(text='CLOSE', bg=self.bgMenu, fg='Tomato', command=lambda:destroyItens())
        btDestroy.place(x=500, y=400)

        #DESTRUI ITENS
        def destroyItens():
            
            lblTitle.destroy()
            lblRevenue.destroy()
            comboRevenue.destroy()

            btSave.destroy()
            btDestroy.destroy()

            self.backGround.destroy()

    # ----------------------- SETOR DE UPDATE DE VALOR -----------------------
    def updateValueSpending(self):

        #CRIAR FUNDO PRETO
        self.createBackGround()

        lblTitle = Label(text='Update Value Spending', font=self.fontStyleUpper, bg=self.bgMenu, fg=self.colorTaps)
        lblTitle.place(x=280, y=100)

        #VALOR
        lblValor = Label(text='Despesa:', font= self.fontDefault, bg=self.bgMenu, fg=self.colorTaps)
        lblValor.place(x=280, y=140)

        etValor = Entry(width=12, font= self.fontDefault) 
        etValor.place(x=280, y=160)

        def save():
            #PEGA O ID
            itemSelecionado = self.treeViewSpendings.selection()[0]
            id = self.treeViewSpendings.item(itemSelecionado, "values")[0]

            valor = -float(etValor.get())

            if messagebox.askquestion('Update Value', F'DESEJAR ALTERA VALOR ID [{id}]?') == 'yes':
                
                #ATUALIZA O VALOR NO BANCO DE DADOS
                self.bancoDados.updateValorSpending(self.currentMonth, id, valor)

                #ATUALIZA AS TABELAS
                self.refreshTables()

                #LIMPA O CAMPO DE VALOR
                etValor.delete(0, END)

                #MENSAGEM DE SUCESSO
                messagebox.showinfo('', 'Atualizado Com Sucesso !')

        #BOTAO DE SALVAMENTO
        btSave = Button(text='SAVE', bg=self.bgMenu, fg='MediumSpringGreen', command=save)
        btSave.place(x=585, y=400)

        #BOTAO PARA DESTRUIR TODOS OS ITENS
        btDestroy = Button(text='CLOSE', bg=self.bgMenu, fg='Tomato', command=lambda:destroyItens())
        btDestroy.place(x=500, y=400)

        #DESTRUI ITENS
        def destroyItens():
            
            lblTitle.destroy()
            lblValor.destroy()
            etValor.destroy()

            btSave.destroy()
            btDestroy.destroy()

            self.backGround.destroy()

    def updateValueRevenue(self):

        #CRIAR FUNDO PRETO
        self.createBackGround()

        lblTitle = Label(text='Update Value Revenue', font=self.fontStyleUpper, bg=self.bgMenu, fg=self.colorTaps)
        lblTitle.place(x=280, y=100)

        #VALOR
        lblValor = Label(text='Valor:', font= self.fontDefault, bg=self.bgMenu, fg=self.colorTaps)
        lblValor.place(x=280, y=140)

        etValor = Entry(width=12, font= self.fontDefault) 
        etValor.place(x=280, y=160)

        def save():
            #PEGA O ID
            itemSelecionado = self.treeViewRevenue.selection()[0]
            id = self.treeViewRevenue.item(itemSelecionado, "values")[0]

            valor = float(etValor.get())

            if messagebox.askquestion('Update Value', F'DESEJAR ALTERA VALOR ID [{id}]?') == 'yes':
                
                #ATUALIZA O VALOR NO BANCO DE DADOS
                self.bancoDados.updateValorRevenue(self.currentMonth, id, valor)

                #ATUALIZA AS TABELAS
                self.refreshTables()

                #LIMPA O CAMPO DE VALOR
                etValor.delete(0, END)

                #MENSAGEM DE SUCESSO
                messagebox.showinfo('', 'Atualizado Com Sucesso !')

        #BOTAO DE SALVAMENTO
        btSave = Button(text='SAVE', bg=self.bgMenu, fg='MediumSpringGreen', command=save)
        btSave.place(x=585, y=400)

        #BOTAO PARA DESTRUIR TODOS OS ITENS
        btDestroy = Button(text='CLOSE', bg=self.bgMenu, fg='Tomato', command=lambda:destroyItens())
        btDestroy.place(x=500, y=400)

        #DESTRUI ITENS
        def destroyItens():
            
            lblTitle.destroy()
            lblValor.destroy()
            etValor.destroy()

            btSave.destroy()
            btDestroy.destroy()

            self.backGround.destroy()

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

        comboDespesa['values'] = self.bancoDados.spendings
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

        comboMes = ttk.Combobox(width= 10, font= self.fontDefault) 

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

        comboRevenue['values'] = self.bancoDados.revenues
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
            #PEGA O ID
            itemSelecionado = self.treeViewSpendings.selection()[0]
            id = self.treeViewSpendings.item(itemSelecionado, "values")[0]
            
            if messagebox.askquestion('', F'Delete Spending ID: {id} ?') == 'yes':
                
                #DELETA O ITEM SELECIONADO    
                self.bancoDados.dropSpending(self.currentMonth, id)

                #ATUALIZAR AS TABELAS
                self.refreshTables() 

        except:
            pass

    def deleteRevenue(self):
        
        #PEGA O ID
        itemSelecionado = self.treeViewRevenue.selection()[0]
        id = self.treeViewRevenue.item(itemSelecionado, "values")[0]
        
        if messagebox.askquestion('', F'Delete Revenue ID: {id} ?') == 'yes':
            
            #DELETA O ITEM SELECIONADO    
            self.bancoDados.dropRevenue(self.currentMonth, id)

            #ATUALIZAR AS TABELAS
            self.refreshTables()                
    
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

    # ----------------------- SETOR DE BACKUP -----------------------
    def generateBackup(self):

        self.windowBackup = Tk()
        self.windowBackup.geometry('230x450+10+10')
        self.windowBackup.resizable(False, False)
        self.windowBackup.title('FINANCE BACKUP')
        
        lblBackup = Label(self.windowBackup, text='BACKUP SECTOR', font='Monaco 15 bold')
        lblBackup.pack()

        lblStatus = Label(self.windowBackup, text='STATUS:')
        lblStatus.place(x=10, y=35)

        lblStatusUpdate = Label(self.windowBackup, text='---', font='Monaco 10 bold')
        lblStatusUpdate.place(x=80, y=35)

        # Using treeview widget 
        self.treeViewBackup = ttk.Treeview(self.windowBackup, selectmode ='browse', height=15) 
        self.treeViewBackup.place(x=10, y=60)

        # Constructing vertical scrollbar 
        # with treeview 
        verscrlbar = ttk.Scrollbar(self.windowBackup, orient ="vertical", command = self.treeViewSpendings.yview) 
        verscrlbar.pack(side ='right', fill ='x') 

        # Configuring treeview 
        self.treeViewBackup.configure(xscrollcommand = verscrlbar.set) 

        # Defining number of columns 
        self.treeViewBackup["columns"] = ("1") 

        # Defining heading 
        self.treeViewBackup['show'] = 'headings'

        self.treeViewBackup.column("1", width = 200, anchor ='c') 
        self.treeViewBackup.heading("1", text ="DEVICES")

        #LISTAR DEVICES
        def listDevices():
            
            devices = self.backup.getDevices()

            for i in devices:
                #INSERE OS DEVICES
                self.treeViewBackup.insert("", 'end', text ="L1", values =(i))

        #LIMPEZA DE TREEVIEW
        def clearAllDevices():

            #PEGA TODOS OS FILHOS
            x = self.treeViewBackup.get_children()

            #VERIFICA SE NÃO ESTÁ FAZIA
            if x != '()':

                #VARRE A LISTA
                for child in x:

                    #DELETA O ITEM CORRESPONDENTE
                    self.treeViewBackup.delete(child)

        def save():

            try:
                #PEGA O ID
                itemSelecionado = self.treeViewBackup.selection()[0]
                nameDevice = self.treeViewBackup.item(itemSelecionado, "values")[0]

                #FUNCAO DE BACKUP
                self.backup.createBackup(nameDevice)

                #EDITAR LABEL DE STATUS
                lblStatusUpdate['text'] = '>> SUCESS <<'
                lblStatusUpdate['fg'] = 'Green'

            except:
                #EDITAR LABEL DE STATUS
                lblStatusUpdate['text'] = '*BACKUP ERROR'
                lblStatusUpdate['fg'] = 'Red'

        def refresh():
            
            #ATUALIZA A LISTA DE DISPOSITIVOS
            clearAllDevices()
            listDevices()

            #EDITAR LABEL DE STATUS
            lblStatusUpdate['text'] = '---'
            lblStatusUpdate['fg'] = 'Black'

        #LISTA TODOS OS DEVICES
        listDevices()

        #REALIZAR O BACKUP
        btBackup = Button(self.windowBackup, text='BACKUP', command=save)
        btBackup.place(x=10, y=390)

        btRefresh = Button(self.windowBackup, text='REFRESH', command=refresh)
        btRefresh.place(x=120, y=390)

        self.windowBackup.mainloop()

if __name__ == "__main__":
    m = months()