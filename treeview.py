# Python program to illustrate the usage of 
# treeview scrollbars using tkinter 

from tkinter import ttk 
import tkinter as tk 
from dataBase import bd



# Creating tkinter window 
window = tk.Tk() 
window.resizable(width = 1, height = 1) 

style = ttk.Style(window)
style.theme_use('clam')

style.configure(    "Treeview",
                    background="Silver",
                    foreground='white',
                    fieldbackground='Silver'
                    )

style.map("Treeview", background=[('selected', 'orange')])

# Using treeview widget 
treev2 = ttk.Treeview(window, selectmode ='browse') 

# Calling pack method w.r.to treeview 
treev2.pack(side ='right') 

# Constructing vertical scrollbar 
# with treeview 
verscrlbar = ttk.Scrollbar(window, 
						orient ="vertical", 
						command = treev2.yview) 

# Calling pack method w.r.to verical 
# scrollbar 
verscrlbar.pack(side ='right', fill ='x') 

# Configuring treeview 
treev2.configure(xscrollcommand = verscrlbar.set) 

# Defining number of columns 
treev2["columns"] = ("1", "2", "3", "4") 

# Defining heading 
treev2['show'] = 'headings'

# Assigning the width and anchor to the 
# respective columns 
treev2.column("1", width = 40, anchor ='c') 
treev2.column("2", width = 120, anchor ='se') 
treev2.column("3", width = 90, anchor ='se') 
treev2.column("4", width = 90, anchor ='se')

# Assigning the heading names to the 
# respective columns 
treev2.heading("1", text ="Id") 
treev2.heading("2", text ="Name") 
treev2.heading("3", text ="Value")
treev2.heading("4", text ="Status")

# columns built 
for i in bd().getListaGastosMes(11,2020):
    treev2.insert("", 'end', text ="L1", values =(i[0], i[2], i[3], i[4]))

def getId():
    itemSelecionado = treev2.selection()[0]
    
    #PEGAR VALORES
    id = int(treev2.item(itemSelecionado, "values")[0])
    print(id)

    #Deletar Item
    #treev2.delete(itemSelecionado)


bt = tk.Button(text='Get', command=getId)
bt.pack()

# Calling mainloop 
window.mainloop() 
