import sys
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

#Arrumando input caso esteja pra Windows e não linux
archive_input = sys.argv[1].replace('\\', '/')

#Criando input_string como utf-8 pra não dar problema com acentos
input_string = FileStream(archive_input, 'utf-8')
lexer = MMSuiteLexer(input_string)
stream = CommonTokenStream(lexer)
parser = MMSuiteParser(stream)

tree = parser.programa()

if parser.getNumberOfSyntaxErrors() > 0:
    print("syntax errors")
else:
    vinterp = VisitorInterp(tree, lexer)
    vinterp.visitPrograma()

print('Fim da compilacao.')


