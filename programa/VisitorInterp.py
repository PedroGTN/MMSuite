from antlr4 import *
from MMSuiteLexer import MMSuiteLexer
from MMSuiteParser import MMSuiteParser
from MMSuiteListener import MMSuiteListener
from antlr4.tree.Tree import TerminalNodeImpl

debug = 0

class VisitorInterp(MMSuiteListener):
    def __init__(self, ctx:MMSuiteParser.ProgramaContext, lexer:MMSuiteLexer):
        self.ctx = ctx
        MMSuiteParser.ProgramaContext.start

    def getTokenName(self, token):
        if isinstance(token, TerminalNode):
            return (token.symbol.type)
        else:
            return 0

    def visitPrograma(self):
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

        # print(self.dict)
        return 

    def visitToken(self, token):
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
        print(line1, line2, line3)