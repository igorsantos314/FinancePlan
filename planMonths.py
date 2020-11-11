from datetime import date
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from dataBase import bd

class months(Frame):

    def __init__(self):

        #OBJETO DE BANCO DE DADOS
        self.bancoDados = bd()

        #DEFAULT
        self.verdeClaro = 'MediumSpringGreen'
        self.fontStyleUpper = 'Courier 20 bold'
        self.tomato = 'Tomato'
        self.gold= 'PaleGoldenrod'
        self.azulClaro = 'PowderBlue'
        self.fontDefault = 'Courier 12'
        self.fontTad = 'Monaco 10 bold'

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
        self.windowMain.geometry('995x450+10+10')
        self.windowMain.resizable(False, False)
        self.windowMain.title('FINANCE')

        #BARRA DE FUNÇÕES
        menubar = Menu(self.windowMain)
        myMenu = Menu(menubar, tearoff=0)

        #Menu de vendedores
        fileMenuFile = Menu(myMenu)
        fileMenuFile.add_command(label='New Spending', command=self.insertDespesa)
        fileMenuFile.add_command(label='New Revenue', command='')

        fileMenuFile.add_separator()
        fileMenuFile.add_command(label='Monthly Report', command=self.createMonthlyReport)

        #fileMenuFile.add_command(label='VALOR', command='lambda: self.windowChangeValor(self.getBarCode(self.listbox.get(ACTIVE)))')

        menubar.add_cascade(label="File", menu=fileMenuFile)

        #FILE MENU DE CAIXAS
        fileMenuBox = Menu(myMenu)
        fileMenuBox.add_command(label='Cash Deposit BOX T', command='')
        fileMenuBox.add_command(label='Cash Deposit BOX E', command='')
        fileMenuBox.add_command(label='Cash Deposit BOX S', command='')
        fileMenuBox.add_command(label='Cash Deposit BOX F', command='')
        fileMenuBox.add_command(label='Edit Box', command='')

        menubar.add_cascade(label="Boxes", menu=fileMenuBox)

        #FILE MENU DE TORNEIRAS
        fileMenuTap = Menu(myMenu)
        fileMenuTap.add_command(label='Edit Name', command='')
        fileMenuTap.add_command(label='Edit Value', command='')
        fileMenuTap.add_command(label='Update Status', command=self.updateStatus)

        fileMenuTap.add_separator()

        fileMenuTap.add_command(label='Del Tap', command='')
        menubar.add_cascade(label="Taps", menu=fileMenuTap)

        #SETAR TITULO DA JANELA PRINCIPAL
        self.lblTitle = Label(text='', font=self.fontStyleUpper)
        self.lblTitle.grid(column=0, row=0, pady=5, padx=10)
        
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

    def keyPressed(self, event):
        l = event.keysym

        if l == 'F2':
            #ADICIONAR NOVA DESPESA
            self.insertDespesa()

        elif l == 'F5':
            #ATUALIZA A LISTA DE GASTOS
            self.insertSpendingListBox()

            #ATUALIZA LISTA DA RECEITA
            self.insertTapsListBox()

        elif l == 'F6':
            #VOLTA UM MES
            self.prevMonth()

        elif l == 'F8':
            #AVANÇA UM MES
            self.nextMonth()
    
    def setTitleWindowMain(self):
        #DEFINE O TITULO
        self.lblTitle['text'] = f'MY FINANCES - {self.currentMonth}/{self.currentYear}'

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
        self.insertTapsListBox()

    def setListBoxSpending(self):
        #LABEL DE GASTOS
        lblGastos = Label(text='WATER TAP', font=self.fontDefault)
        lblGastos.grid(column=0, row=1, pady=5, padx=10)

        self.listboxtTaps = Listbox(self.windowMain, height=20, width=50, font= self.fontDefault, bg='red', fg='white')
        self.listboxtTaps.grid(column=0, row=2, pady=5, padx=10)

    def setListBoxT(self):
        #LABEL DE RECEITA DO MES
        lblReceita = Label(text='BOX T', font=self.fontDefault)
        lblReceita.grid(column=1, row=1, pady=5, padx=10)

        self.listboxBox = Listbox(self.windowMain, height=20, width=45, font= self.fontDefault, bg='green', fg='white')
        self.listboxBox.grid(column=1, row=2, pady=5, padx=5)

    """def setListBoxESF(self):

        #LABEL DAS CAIXAS
        lblReceita = Label(text='BOX E/S/F', font=self.fontDefault)
        lblReceita.grid(column=1, row=3, pady=5, padx=10)

        self.listboxBox = Listbox(self.windowMain, height=12, width=45, font= self.fontDefault, bg='LemonChiffon')
        self.listboxBox.grid(column=1, row=4, pady=5, padx=5)"""

    def insertTapsListBox(self, m=None, y=None):

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
            valor = "R${}{}".format(valor, " " * (8 - len(valor)))

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
            valor = "R${}{}".format(valor, " " * (8 - len(valor)))

            statusPag = "{}{}".format(i[4], " " * (12 - len(i[4])))

            self.listboxtTaps.insert("end", F'{id}{nome}{valor}{statusPag}')

        #SOMA DAS DESPESAS
        total = self.bancoDados.getGastosMes(m, y)

        #INSERIR DESPESAS NO LISTBOX
        self.listboxtTaps.insert("end", '---------------------------------------------------')
        space = ' ' * 24

        self.listboxtTaps.insert("end", F' TOTAL: {space} R${total}')

    def updateStatus(self):

        try:
            indice = self.listboxtTaps.curselection()[0]
            id = int(self.listboxtTaps.get(indice).split(" ")[0])
            
            #ATUALIZAR O STATUS        
            self.bancoDados.updateStatus(self.currentMonth, id)

            #ATUALIZAR LISTBOX
            self.insertSpendingListBox()

        except:
            pass

    def insertDespesa(self):

        self.windowDespesa = Tk()
        self.windowDespesa.geometry('300x200+10+10')
        self.windowDespesa.resizable(False, False)
        self.windowDespesa.title('ADD DESPESA')

        #Mes
        lblMes = Label(self.windowDespesa, text='Mês:')
        lblMes.place(x=20, y=20)

        comboMes = ttk.Combobox(self.windowDespesa, width= 15) 

        comboMes['values'] = tuple([i for i in range(1, 12)])
        comboMes.current(self.month-1)
        comboMes.place(x=20, y=40)

        #Ano
        lblAno = Label(self.windowDespesa, text='Ano:')
        lblAno.place(x=170, y=20)

        comboAno = ttk.Combobox(self.windowDespesa, width=12) 

        comboAno['values'] = tuple(['{}'.format(i) for i in range(2020, 2051)])
        comboAno.current(0)
        comboAno.place(x=170, y=40)

        #DESPESA
        lblDespesa = Label(self.windowDespesa, text='Despesa:')
        lblDespesa.place(x=20, y=70)

        comboDespesa = ttk.Combobox(self.windowDespesa, width=12) 

        comboDespesa['values'] = tuple(['ALIMENTAÇÃO', 'COMBUSTIVEL', 'CARTÃO -', 'SAUDE', 'OUTROS'])
        comboDespesa.current(0)
        comboDespesa.place(x=20, y=90)

        #VALOR
        lblValor = Label(self.windowDespesa, text='Valor:')
        lblValor.place(x=170, y=70)

        etValor = Entry(self.windowDespesa, width=9)
        etValor.place(x=170, y=90)

        #MACRO
        lblMacro = Label(self.windowDespesa, text='Macro:')
        lblMacro.place(x=20, y=120)

        comboMacro = ttk.Combobox(self.windowDespesa, width=12) 

        comboMacro['values'] = tuple([i for i in range(1, 24)])
        comboMacro.current(0)
        comboMacro.place(x=20, y=140)

        def save():

            try:
                #QUANTIDAD ED EPARCELAS
                iteracoes = int(comboMacro.get())
                
                #INFORMAÇẼOS DA COMPRA
                mes = int(comboMes.get())
                ano = int(comboAno.get())
                item  = comboDespesa.get().upper()[:24]
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

            except:
                messagebox.showerror('', 'Ocorreu um Erro !')

        #BOTAO SE SALVAMENTO
        btSave = Button(self.windowDespesa, text='SALVAR', bg='MediumSpringGreen', command=save)
        btSave.place(x=170, y=140)

        self.windowDespesa.mainloop() 

    def createMonthlyReport(self):

        try:
            #CRIAR CSV
            self.bancoDados.createCSV(self.currentMonth, self.currentYear)

            #MENSAGEM DE SUCESSO
            messagebox.showinfo('SUCESSO', f'RELATÓRIO MENSAL DE {self.currentMonth}/{self.currentYear} CRIADO!')

        except:
            messagebox.showerror('', 'OCORREU UM ERRO :(')

if __name__ == "__main__":
    m = months()