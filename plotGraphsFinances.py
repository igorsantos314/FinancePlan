from pylab import *

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