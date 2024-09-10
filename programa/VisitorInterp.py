from antlr4 import *
from antlr4.tree.Tree import TerminalNodeImpl

from MMSuiteLexer import MMSuiteLexer
from MMSuiteParser import MMSuiteParser
from MMSuiteListener import MMSuiteListener


debug = 2

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
        with open("lib/" + self.func_name + ".py", 'w') as out_file:
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

        if debug == 2:
            print(line1, line2, line3)

        with open("lib/" + self.func_name + ".py", 'a') as out_file:
            if line3[0] == 'func': # verificando se o primeiro token da linha é a palavra func para saber que estamos tratando de uma declaração de função
                out_file.write('\n')
                open_args = line3.index('(') # achando o primeiro parenteses da função
                args = []
                for i in range(open_args + 1, len(line3), 2): # iterando apenas pelos agumentos da função
                    args.append(line3[i])
                    self.variaveis.append(line3[1]) # salva as variaveis para analizar outras linhas
                
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
                        out_file.write(args + '\n')
                    elif line1[2] == '19':
                        out_file.write(line3[2] + '\n')
                    elif line3[2] in self.functions.keys():
                        args =''
                        first_arg_ind = line3.index('(') + 1
                        last_ind = line3.index(')')
                        for i in range(first_arg_ind, last_ind, 2):
                            args += line3[i] + ' + " " + '
                        out_file.write('mms_exec(\"python3 lib/'+ line3[2] +'.py \" + ' + args[:-2] + ', 0'+')\n')
                    elif line3[2] in self.variaveis: 
                        out_file.write(line3[2] + '\n')
                else: #temos uma execucao de funcao
                    args = ' '
                    first_arg_ind = line3.index('(') + 1
                    last_ind = line3.index(')')
                    for i in range(first_arg_ind, last_ind, 2):
                            args += line3[i] + ' + " " + '
                    out_file.write('mms_exec(\"python3 lib/'+ line3[0] +'.py \" + ' + args[:-2] + ', 0'+')\n')
                    