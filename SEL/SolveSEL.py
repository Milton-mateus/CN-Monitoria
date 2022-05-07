import enum
from unicodedata import name
from matplotlib.pyplot import pause, text
import numpy as np
import json
import pathlib

class SEL():
    def __init__(self, Data):
        self.Data = Data
        self.Neq = self.Data['Neq']
        self.tol = self.Data['tol']
        self.Amatrix = np.zeros([self.Neq, self.Neq])
        self.Bvec = np.zeros([1,self.Neq])
        self.coefs_att()
        self.B_att()
    
    def coefs_att(self):
        for i, coefs in enumerate(self.Data['coefs']):
            for j,coef in enumerate(coefs):
                self.Amatrix[i,j] = coef
    
    def B_att(self):
        for j,b in enumerate(self.Data['values']):
            self.Bvec[0,j] = b

    def Criterio_linhas(self):
        self.Beta = np.zeros(self.Neq)
        self.textBeta = "Critério das linhas \nInício do cálculo de beta: \n\n"
        for i,line in enumerate(self.Amatrix):
            beta_line = 0
            self.textBeta += "Beta" + str(i+1) + " = "
            cont = 0
            for j,coef in enumerate(line):
                if i != j:
                    cont += 1
                    beta_line += abs(coef) / abs(line[i])
                    self.textBeta += "(|" + str(coef) + "| / |" + str(line[i])+ "|)"
                    if cont != self.Neq-1:
                        self.textBeta += " + "
            self.textBeta += " = " + str(beta_line) + "\n"
            self.Beta[i] = beta_line
        self.Beta_max = max(self.Beta)
        if self.Beta_max < 1:
            self.textBeta += "\nA matriz inserida atende ao critério das linhas, tal que Beta_max = " + str(self.Beta_max) + " < 1"
        elif self.Beta_max == 1:
            self.textBeta += "\nA matriz inserida não atende ao critério das linhas, tal que Beta_max = " + str(self.Beta_max) + " = 1"
        else:
            self.textBeta += "\nA matriz inserida não atende ao critério das linhas, tal que Beta_max = " + str(self.Beta_max) + " > 1"


    def Criterio_colunas(self):
        self.Beta = np.zeros(self.Neq)
        self.textBeta = "Critério das colunas \nInício do cálculo de beta: \n\n"
        for i in range (self.Neq):
            beta_line = 0
            self.textBeta += "Beta" + str(i+1) + " = "
            cont = 0
            for j in range(self.Neq):
                if i != j:
                    cont += 1
                    beta_line += abs(self.Amatrix[j,i]) / abs(self.Amatrix[i,i])
                    self.textBeta += "(|" + str(self.Amatrix[j,i]) + "| / |" + str(self.Amatrix[i,i])+ "|)"
                    if cont != self.Neq-1:
                        self.textBeta += " + "
            self.textBeta += " = " + str(beta_line) + "\n"
            self.Beta[i] = beta_line
        self.Beta_max = max(self.Beta)
        if self.Beta_max < 1:
            self.textBeta += "\nA matriz inserida atende ao critério das colunas, tal que Beta_max = " + str(self.Beta_max) + " < 1"
        elif self.Beta_max == 1:
            self.textBeta += "\nA matriz inserida não atende ao critério das colunas, tal que Beta_max = " + str(self.Beta_max) + " = 1"
        else:
            self.textBeta += "\nA matriz inserida não atende ao critério das colunas, tal que Beta_max = " + str(self.Beta_max) + " > 1"


    def Criterio_Sassenfeld(self):
        self.Beta = np.zeros(self.Neq)
        self.textBeta = "Critério das Sassenfeld \nInício do cálculo de beta: \n\n"
        for i,line in enumerate(self.Amatrix):
            beta_line = 0
            self.textBeta += "Beta" + str(i+1) + " = "
            cont = 0
            for j,coef in enumerate(line):
                if i != j:
                    cont += 1
                    if i < j:
                        beta_line += abs(coef) / abs(line[i])
                        self.textBeta += "(|" + str(coef) + "| / |" + str(line[i])+ "|)"
                    else:
                        beta_line += abs(coef) * self.Beta[j] / abs(line[i])
                        self.textBeta += "(|" + str(coef) + "| / |" + str(line[i]) + "|)" + " * " + str(self.Beta[j])                    
                    if cont != self.Neq-1:
                        self.textBeta += " + "
            self.textBeta += " = " + str(beta_line) + "\n"
            self.Beta[i] = beta_line
        self.Beta_max = max(self.Beta)
        if self.Beta_max < 1:
            self.textBeta += "\nA matriz inserida atende ao critério das linhas, tal que Beta_max = " + str(self.Beta_max) + " < 1"
        elif self.Beta_max == 1:
            self.textBeta += "\nA matriz inserida não atende ao critério das linhas, tal que Beta_max = " + str(self.Beta_max) + " = 1"
        else:
            self.textBeta += "\nA matriz inserida não atende ao critério das linhas, tal que Beta_max = " + str(self.Beta_max) + " > 1"
        
    

    def print_criterios(self):
        print("\n\n")
        self.Criterio_linhas()
        print(self.textBeta)
        print("\n\n------------------------------------------------------------------------\n\n")
        self.Criterio_colunas()
        print(self.textBeta)
        print("\n\n------------------------------------------------------------------------\n\n")
        self.Criterio_Sassenfeld()
        print(self.textBeta)

def ReadJson():
    # namefile = input("Insira o nome do arquivo: ")
    namefile = "Example"
    namefile += ".json"
    datapath=pathlib.Path(__file__).parent / namefile
    InputData = json.load(open(datapath))
    return InputData


def Create_MnV():

    pass

if __name__ == "__main__":
    # Lê o arquivo
    Data = ReadJson()
    # Monta as matrizes e vetores
    SistemaEqLineares = SEL(Data)
    SistemaEqLineares.print_criterios()
    pause