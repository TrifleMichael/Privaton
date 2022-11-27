import simplerlangParser
from simplerlangListener import simplerlangListener
from simplerlangParser import simplerlangParser

class SimplerlangListenerExtended(simplerlangListener):
    variableNamesMap = {}
    tmp = 0

    def exitLet(self, ctx:simplerlangParser.LetContext):
        print("Analyzing let", ctx.getText())
        self.variableNamesMap[ctx.NAME().__str__()] = self.tmp
        print("Set", ctx.NAME().__str__(), "as", self.tmp)

    def exitSmall_expr(self, ctx:simplerlangParser.Small_exprContext):
        print("Analyzing small_expr", ctx.getText())
        # self.tmp = eval(ctx.getText())

        # SINGLE VALUE
        if ctx.getChildCount() == 1:
            if isinstance(ctx.children[0], simplerlangParser.VarContext):
                # Single NAME
                if ctx.children[0].NAME() != None:
                    self.tmp = self.variableNamesMap[ctx.children[0].NAME().__str__()]
                    print("read", ctx.children[0].NAME().__str__(), "as", self.tmp)
                # Single constant
                else:
                    self.tmp = ctx.children[0].getText()
                    print("read",ctx.children[0].getText(), "as", self.tmp)

        # # Binop
        if ctx.getChildCount() == 3:
            # print("Tripe")
            if isinstance(ctx.children[0], simplerlangParser.VarContext):
                # NAME and binop
                if ctx.children[0].NAME() != None:
                    secondTmp = self.variableNamesMap[ctx.children[0].NAME().__str__()]
                    self.tmp = eval(str(secondTmp) + ctx.bin_opr().getText() + str(self.tmp))
                    print("evaluated", str(secondTmp) + ctx.bin_opr().getText() + str(self.tmp), "as", self.tmp)
                # Constant and binop
                else:
                    print("Gonna evaluate", ctx.children[0].getText() + ctx.bin_opr().getText() + str(self.tmp))
                    debug = str(self.tmp)
                    self.tmp = eval(ctx.children[0].getText() + ctx.bin_opr().getText() + str(self.tmp))
                    print("read",ctx.children[0].getText() + ctx.bin_opr().getText() + debug, "as", self.tmp)


    def exitShow(self, ctx:simplerlangParser.ShowContext):
        print(self.tmp)


