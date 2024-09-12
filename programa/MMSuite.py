import sys
import os
import subprocess

from antlr4 import *
from antlr4.error.ErrorListener import ProxyErrorListener

from MMSuiteLexer import MMSuiteLexer
from MMSuiteParser import MMSuiteParser
from VisitorInterp import VisitorInterp
from execute_func import shell_exec
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

current_dir = os.path.dirname(__file__)
mmlib = current_dir +  "/lib/funcloc.mmlib"
debug = 0

if len(sys.argv) > 1: # se for necessaria a compilacao
    if sys.argv[1] == 'add':
        #Arrumando input caso esteja pra Windows e não linux
        archive_input = sys.argv[-1].replace('\\', '/')

        #Criando input_string como utf-8 pra não dar problema com acentos
        
        input_string = FileStream(archive_input, 'utf-8')
        func_name = archive_input.split('/')[-1][:-4] # captura o nome do arquivo onde esta a funcao
        lexer = MMSuiteLexer(input_string)
        stream = CommonTokenStream(lexer)
        parser = MMSuiteParser(stream)

        tree = parser.programa()

        if parser.getNumberOfSyntaxErrors() > 0: # verifica se houve erros sintáticos, cancelando a compilação caso haja erros
            print("Erros de sintaxe")
        else:
            vinterp = VisitorInterp(tree, lexer, func_name, mmlib) # começa a verificação e compilação do código sem erros sintáticos ou léxicos 
            vinterp.visitPrograma()
            print('Compilacao concluida com sucesso.') 


    elif sys.argv[1] == 'del':
        functions = dict()
        with open(mmlib, 'r') as libarq:
            lines = libarq.readlines()
            for line in lines:
                if line is None: pass
                line_split = line.split()
                functions[line_split[0]] = [line_split[1],line_split[2], line_split[-1]]
        
        if not sys.argv[2] in functions.keys():
            print("Já tirou irmão")
            exit(42)

        functions.pop(sys.argv[2]) # remove a função da lista de funções
        os.remove(current_dir + '/lib/' + sys.argv[2] + '.py')
        
        with open(mmlib, 'w') as libarq:
            for key in functions.keys(): # for usado para criar a biblioteca de funções sem a função que foi removida 
                libarq.write(key + ' ' + functions[key][0] + ' ' + functions[key][1] + ' ' + functions[key][2] + '\n') 
    
    else:
        functions = dict()
        with open(mmlib, 'r') as libarq:
            lines = libarq.readlines()
            for line in lines:
                if line is None: pass
                line_split = line.split()
                functions[line_split[0]] = [line_split[1],line_split[2], line_split[-1]]
        if sys.argv[1] in functions.keys(): 
            function = ''
            for i in sys.argv[1:]:
                function += i + ' '

            func_split = function.split()
            func_args = functions[func_split[0]]

            if not func_split[0] in functions.keys():
                print("Função nem existe mano")
            
            # if len(func_split) != int(func_args[0]) + 1:
            #     print("ficou sem argumento, paizao...")
            #     print(len(func_split), int(func_args[0]))

            cmd = ["python3", current_dir + "/lib/" + func_args[-1]] + func_split[1:]
            saida = shell_exec(cmd, functions[func_split[0]][2])
            print(saida)
            if debug:
                print('stdout:', saida)
                print(cmd)


else: # se uma funcao for ser interpretada
    functions = dict()
    with open(mmlib, 'r') as libarq:
        lines = libarq.readlines()
        for line in lines:
            if line is None: pass
            line_split = line.split()
            functions[line_split[0]] = [line_split[1],line_split[2], line_split[-1]] 
    while (True):
        function = input('>>>')
        if function == 'exit': exit()
        func_split = function.split()
        func_args = functions[func_split[0]]

        if not func_split[0] in functions.keys():
            print("Função nem existe mano")
        
        # if len(func_split) != int(func_args[0]) + 1 or int(func_args[0]) == 0:
        #     print("ficou sem argumento, paizao...")
        #     print(len(func_split), int(func_args[0]))

        cmd = ["python3", current_dir + "/lib/" + func_args[-1]] + func_split[1:]
        saida = shell_exec(cmd, functions[func_split[0]][2])

        if debug:
            print('stdout:', saida)
            print(cmd)