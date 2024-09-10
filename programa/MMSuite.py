import sys
import os
import subprocess

from antlr4 import *
from antlr4.error.ErrorListener import ProxyErrorListener

from MMSuiteLexer import MMSuiteLexer
from MMSuiteParser import MMSuiteParser
from VisitorInterp import VisitorInterp
#Importanto error listener customizado
#para poder ter mensagens de erro customizadas
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# from JanderErrorListener import * 
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#Importanto classe de vocabulary para poder 
#saber o nome de um tipo de token
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# from Vocabulary import Vocabulary
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
mmlib = "lib/funcloc.mmlib"
if len(sys.argv) > 1: # se for necessaria a compilacao
    #Arrumando input caso esteja pra Windows e não linux
    archive_input = sys.argv[1].replace('\\', '/')

    #Criando input_string como utf-8 pra não dar problema com acentos
    
    input_string = FileStream(archive_input, 'utf-8')
    func_name = archive_input.split('/')[-1][:-4] # captura o nome do arquivo onde esta a funcao
    lexer = MMSuiteLexer(input_string)
    stream = CommonTokenStream(lexer)
    parser = MMSuiteParser(stream)

    tree = parser.programa()

    if parser.getNumberOfSyntaxErrors() > 0:
        print("syntax errors")
    else:
        vinterp = VisitorInterp(tree, lexer, func_name, mmlib)
        vinterp.visitPrograma()

    print('Fim da compilacao.')

else: # se uma funcao for ser interpretada
    functions = dict()
    with open(mmlib, 'r') as libarq:
        lines = libarq.readlines()
        for line in lines:
            if line is None: pass
            line_split = line.split()
            functions[line_split[0]] = [line_split[1],line_split[2], line_split[-1]] # line_split[2] detecta se deve haver retorno 
    while (True):
        function = input('>>>')
        if function == 'exit': exit()
        func_split = function.split()
        func_args = functions[func_split[0]]

        if not func_split[0] in functions.keys():
            print("Eu tenho um anuncio a fazer sobre shadow o ouriço... ele gerou um erro na minha esposa.")
        
        if len(func_split) != int(func_args[0]) + 1:
            print("ficou sem argumento, paizao...")
            print(len(func_split), int(func_args[0]))

        cmd = ["python3", "lib/" + func_args[-1]] + func_split[1:]

        cmd_exec = ''

        for i in cmd:
            cmd_exec += i + ' '
        #os.system(cmd_exec)
        
        process = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        saida = stdout.decode('utf-8')

        # DAR UM JEITO DE CAPTURAR O STDOUT DESSA FUNCAO

        print('stdout:', saida)
        print(cmd)