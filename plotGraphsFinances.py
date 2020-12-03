from pylab import *
import numpy as np
from random import randint

class plotGraphs:
    
    def __init__(self):
        #OBJETO DE BANCO DE DADOS
        #self.bancoDados = bd()
        pass

    def generateGraph(self, tupleData, tupleIndices, titleGraph, xlabel_str, ylabel_str):
        pos = arange(len(tupleData)) + .5

        valores = tupleData
        topicos = tupleIndices

        #GERAR GRAFICO
        barh(pos, valores, align='center', color='Orange')
        yticks(pos, topicos)

        #INFORMAÇÕES
        title(titleGraph)
        xlabel(xlabel_str)
        ylabel(ylabel_str)

        #LINHAS CORTANDO O GRÁFICOs
        grid(True)

        #EXIBIR GRAFICO
        show()

    def generateGraphYear(self, revenue, spending):
        
        #DADOS DA AMOSTRAGEM
        #REVENUE E SPENDING
        months = ['JAN', 'FEV', 'MARC', 'ABR', 'MAI', 'JUN', 'JUL', 'AGO', 'SET', 'OUT', 'NOV', 'DEZ']

        barWidth = 0.30
        plt.figure(figsize=(10,5))

        #POSICAO DAS BARRAS
        r1 = np.arange(len(revenue))
        r2 = [(x + barWidth) for x in r1]

        #CRIANDO BARRAS
        plt.bar(r1, revenue, color='Green', width=barWidth, label='REVENUE')
        plt.bar(r2, spending, color='Red', width=barWidth, label='SPENGING')

        #ADICIONANDO LEGENDAS AS BARRAS
        plt.xlabel('MONTHS')
        plt.xticks([r + barWidth for r in range(len(revenue))], months)
        plt.ylabel('VALUE R$')
        plt.title('GRAPH OF YEAR')

        #CRIANDO E EXIBINDO O GRAFICO
        plt.legend()
        plt.show()

p = plotGraphs()
p.generateGraphYear([randint(0, 1000) for i in range(12)], [randint(0, 1000) for i in range(12)])