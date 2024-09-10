from antlr4 import *
from MMSuiteLexer import MMSuiteLexer
from MMSuiteParser import MMSuiteParser
from MMSuiteListener import MMSuiteListener
from antlr4.tree.Tree import TerminalNodeImpl

debug = 0

class VisitorInterp(MMSuiteListener):
    def __init__(self, ctx:MMSuiteParser.ProgramaContext, lexer:MMSuiteLexer, func_name, mmlib):
        self.ctx = ctx
        MMSuiteParser.ProgramaContext.start
        self.functions = self.listfunctions(mmlib)
        self.funcarchive = mmlib
        self.variaveis = []
        self.func_name = func_name
        self.initarq()
        self.func_desc = [func_name, 0, 0, func_name + '.py']

    def initarq(self):
        with open("lib/" + self.func_name + ".py", 'w') as out_file:
            out_file.write("import os\nimport sys\n\n")

            

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
        Ta ligado o que isso faz
        """
        if isinstance(token, TerminalNode):
            return (token.symbol.type)
        else:
            return 0

    def visitPrograma(self):
        """
        Funcao que itera pelas linhas as tokenizando e entao as envia para analise
        """
        for i in range(self.ctx.getChildCount()):
            for j in range(self.ctx.getChild(i).getChildCount()):
                
                text, text2 = self.visitToken(self.ctx.getChild(i).getChild(j))
                if debug>1:
                    print(text)
                line_split = []
                for k in text.split():
                    line_split.append(k.split('|'))
                line, line2 = map(list, zip(*line_split))
            
                self.analyzeLine(line, line2, text2.split())
        
        with open(self.funcarchive, 'a') as lib:
            for i in self.func_desc:
                lib.write(str(i) + ' ')
            lib.write('\n')

        # print(self.dict)
        return 

    def visitToken(self, token):
        """
        Tokeniza as linas em um vetor de termos separados

            Args:
            Param1 (ANTLR Token): Token criado pelo ANTLR

            Returns:
            Param1 (Array Str): Tokens em forma de string
        """
        ret = self.getTokenName(token)

        if isinstance(token, TerminalNodeImpl):
            token_mesmo = token.getParent().start
            line = str(token_mesmo.line)
        else:
            line = '-1'
            
        if ret > 0:
            text = str(ret) + '|' + line + " "
            text2 = token.getText() + " "
        else:
            text = ''
            text2 = ''
        if not isinstance(token, TerminalNode):
            for i in range(token.getChildCount()):
                text_final = self.visitToken(token.getChild(i))
                text += text_final[0]
                text2 += text_final[1]

        return [text,text2]

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
        with open("lib/" + self.func_name + ".py", 'a') as out_file:
            if line3[0] == 'func':
                open_args = line3.index('(')
                args = []
                for i in range(open_args + 1, len(line3), 2):
                    args.append(line3[i])
                    self.variaveis.append(line3[1]) # salva as variaveis para analizar outras linhas
                print(args)

                self.func_desc[1] = len(args)

                for i in range(len(args)):
                    out_file.write(args[i] + ' = ' + 'sys.argv[' + str(i+1) + ']\n') # passa ao python os argumentos da funcao
            elif line3[0] == 'python':
                open_args = line3.index('(')
                for i in range(open_args + 1, len(line3), 2):
                    if line1[i] == '16':
                        out_file.write(line3[i][1:-1])
                    else:
                        out_file.write(line3[i])
        # print(line1, line2, line3)