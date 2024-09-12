from antlr4 import *
from antlr4.tree.Tree import TerminalNodeImpl

from MMSuiteLexer import MMSuiteLexer
from MMSuiteParser import MMSuiteParser
from MMSuiteListener import MMSuiteListener

import os


debug = 0
current_dir = os.path.dirname(__file__)

class VisitorInterp(MMSuiteListener):
    def __init__(self, ctx:MMSuiteParser.ProgramaContext, lexer:MMSuiteLexer, func_name, mmlib):
        self.ctx = ctx
        MMSuiteParser.ProgramaContext.start
        self.functions = self.listfunctions(mmlib) # inicializa a lista de funções disponíveis na biblioteca da linguagem

        if func_name in self.functions.keys(): # verifica se a função que será criada já está na biblioteca
            print("Nome de funcao incompativel, já existe uma funcao com esse nome.")
            print("Compilacao cancelada.")
            exit(1)

        self.funcarchive = mmlib # nome do arquivo de funções
        self.variaveis = [] # vetor onde serão guardadas as variáveis para verificação de existência
        self.func_name = func_name # nome da função que será adicionada
        self.initarq()
        self.func_desc = [func_name, 0, 0, func_name + '.py'] # inicializa a descrição da função que será adicionada formatação: nome num_argumentos retorno(sim/não) nome_arquivo_python

    def initarq(self):
        """
        inicializa o cabeçário do arquivo python correspondente à função com imports básicos para o funcionamento
        """
        with open(current_dir + "/lib/" + self.func_name + ".py", 'w') as out_file:
            out_file.write("import os\nimport sys\nfrom execute_func import mms_exec\n\n")

            

    def listfunctions(self, mmlib):
        """
        Funcao que acessa a biblioteca da linguagem e lista as funcoes disponiveis

            Args:
            Param1 (Str): Arquivo de biblioteca da linguagem

            Return:
            Param1 (Dict): Lista de funcoes
        """
        functions = dict()
        with open(mmlib, 'r') as libarq:
            lines = libarq.readlines()
            for line in lines:
                if line is None: pass
                line_split = line.split()
                functions[line_split[0]] = [line_split[1],line_split[2]] # line_split[2] detecta se deve haver retorno 
        return functions

    def getTokenName(self, token):
        """
        recebe um token do ANTLR e retorna o número que corresponde aquele token dentro das definições da gramática
        """
        if isinstance(token, TerminalNode):
            return (token.symbol.type)
        else:
            return 0

    def visitPrograma(self):
        """
        Funcao que itera pelas linhas as tokenizando e entao as envia para analise
        """
        for i in range(self.ctx.getChildCount()): # itera pelos filhos do programa
            for j in range(self.ctx.getChild(i).getChildCount()): # para cada filho do programa itera por seus filhos tokenizando eles em arrays de strings
                
                text, text2 = self.visitToken(self.ctx.getChild(i).getChild(j))
                if debug>1:
                    print(text)
                line_split = []
                for k in text.split():
                    line_split.append(k.split('|'))
                line, line2 = map(list, zip(*line_split))
            
                self.analyzeLine(line, line2, text2.split())
        
        with open(self.funcarchive, 'a') as lib: # escreve a função que foi descrita como parte da lib
            for i in self.func_desc:
                lib.write(str(i) + ' ')
            lib.write('\n')

        # print(self.dict)
        return 

    def visitToken(self, token):
        """
        Recebe um nó da árvore do antlr e visita cada nó folha colocando-os como várias strings em uma array i.e. tokeniza as folhas

            Args:
            Param1 (ANTLR Token): Nó da árvore criada pelo ANTLR

            Returns:
            Param1 (Array Str): Folhas filhas deste nó em forma de string
        """
        ret = self.getTokenName(token) # recebe o identificador do token

        if isinstance(token, TerminalNodeImpl): # verifica se é uma folha
            token_mesmo = token.getParent().start
            line = str(token_mesmo.line)
        else:
            line = '-1'
            
        if ret > 0: # nós folhas possuem identificador maior que zero, logo apenas irá salvar caso seja folha
            text = str(ret) + '|' + line + " "
            text2 = token.getText() + " "
        else:
            text = ''
            text2 = ''
        if not isinstance(token, TerminalNode):
            for i in range(token.getChildCount()):
                text_final = self.visitToken(token.getChild(i)) # recursão para conseguir os outros tokens
                text += text_final[0]
                text2 += text_final[1]

        return [text,text2] # tokens como strings e identificadores de tipo da gramática sendo retornados

    def analyzeLine(self, line1, line2, line3):
        """
        Faz analise dos tokens de forma a executar as funcoes da linguagem. salva as variaveis usadas em self.variaveis
        passa ao python os argumentos da funcao.

            Args:
            Param1 (Array Str): Tipos segundo a gramatica ANTLR.
            Param2 (Array Str): A linha de cada token.
            Param3 (Array Str): A string de cada linha tokenizada.

            Returns:

            Raises:
        """

        i = 0
        while(i < len(line3)):
            if '\'' in line3[i]:
                if line3[i][-1] == '\'':
                    break
                j = i + 1
                while(j < len(line3)):
                    if '\'' in line3[j]:
                        break
                    j += 1
                for k in range(i, j):
                    line3[i] = line3[i] + ' ' + line3[i+1]
                    line3.pop(i+1)

            i += 1            

        if debug == 2:
            print(line1, line2, line3)

        with open(current_dir + "/lib/" + self.func_name + ".py", 'a') as out_file:
            if line3[0] == 'func': # verificando se o primeiro token da linha é a palavra func para saber que estamos tratando de uma declaração de função
                out_file.write('\n')
                open_args = line3.index('(') # achando o primeiro parenteses da função
                args = []
                for i in range(open_args + 1, len(line3), 2): # iterando apenas pelos agumentos da função
                    args.append(line3[i])
                    self.variaveis.append(line3[i]) # salva as variaveis para analizar outras linhas
                
                if debug == 1:
                    print(args)# printa o vetor de argumentos

                self.func_desc[1] = len(args)# atualiza a descrição da função atual colocando o número de argumentos que ela recebe

                for i in range(len(args)):
                    out_file.write(args[i] + ' = ' + 'sys.argv[' + str(i+1) + ']\n') # passa ao python os argumentos da funcao como entradas do stdin

            elif line3[0] == 'python': # verificando se é uma linha de python sendo passada diretamente para o programa
                open_args = line3.index('(') # achando o primeiro parenteses da declaração
                for i in range(open_args + 1, len(line3), 2):
                    out_file.write(line3[i][1:-1]) # removendo as aspas simples
            elif line3[0] == 'import':
                out_file.write('import ' + line3[-1][1:-1] + '\n')
            elif line3[0] == 'from':
                out_file.write('from ' + line3[1][1:-1] +  ' import ' + line3[-1][1:-1] + '\n')
            elif line3[0] == 'return': # essa eh a lei do retorno, nao adianta chorar
                self.func_desc[2] = 1
                out_file.write('print(' + line3[1] + ')\n')
            elif line1[0] == '18':
                if line3[1] == '=':
                    self.variaveis.append(line3[0])
                    out_file.write(line3[0] + ' = ')
                    if '+' in line3:
                        args = ''
                        for i in range(2, len(line3)):
                            args += line3[i] + ' '
                            if line1[i] == '18' and not line3[i] in self.variaveis and line3[i] != '+': #verificando se a variável de string existe antes de concatená-la 
                                print("Variável não declarada anteriormente tentando ser usada \"" + line3[i] + "\" na linha " + line2[i])
                                print("Compilação abortada")
                                exit(1)

                        out_file.write(args + '\n')
                    elif line1[2] == '19':
                        out_file.write(line3[2] + '\n')
                    elif line3[2] in self.functions.keys():
                        args = ''
                        first_arg_ind = line3.index('(') + 1
                        last_ind = line3.index(')')
                        for i in range(first_arg_ind, last_ind, 2):
                            args += line3[i] + ' + " " + '
                        out_file.write('mms_exec(\"python3 ' + current_dir + '/lib/'+ line3[2] +'.py \" + ' + args[:-2] + ', 0'+')\n')
                    elif line3[2] in self.variaveis: 
                        out_file.write(line3[2] + '\n')
                    else: # Análise semântica sendo realizada
                        print("Função ou variável não declarada anteriormente tentando ser usada")
                        print(line3[2] + " encontrado na linha " + line2[2] + "\nCompilação abortada")
                        exit(1)
                else: #temos uma execucao de funcao
                    if not line3[0] in self.functions.keys(): #verificando se a função realmente existe antes de executá-la 
                        print("Função desconhecida sendo executada \"" + line3[0] + "\" na linha " + line2[0] + "\nCompilação abortada")
                        exit(1)
                    args = ' '
                    first_arg_ind = line3.index('(') + 1
                    last_ind = line3.index(')')

                    arg_count = 0
                    for i in range(first_arg_ind, last_ind, 2):
                        args += line3[i] + ' + " " + '
                        arg_count += 1

                    if arg_count != self.functions[line3[0]][0] and int(self.functions[line3[0]][0]): #verificando se o número de argumentos passados é o mesmo que a função precisa
                        print("Número errado de argumentos usados na chamada da função \"" + line3[0] + "\" na linha " + line2[0])
                        print("Compilação abortada")
                        exit(1)

                    out_file.write('mms_exec(\"python3 ' + current_dir + '/lib/'+ line3[0] +'.py \" + ' + args[:-2] + ', 0'+')\n')
                    