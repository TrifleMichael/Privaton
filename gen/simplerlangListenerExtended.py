import simplerlangParser
from simplerlangListener import simplerlangListener
from simplerlangParser import simplerlangParser


class SimplerlangListenerExtended(simplerlangListener):
    variableNamesMap = {}
    If_block2EvaluationMap = {}
    blockIgnoreMap = {}
    tmp = 0  # Holds value of the last small statement
    ignoreBlockDepth = 0

    def exitLet(self, ctx: simplerlangParser.LetContext):
        if self.ignoreBlockDepth == 0:
            self.variableNamesMap[ctx.NAME().__str__()] = self.tmp

    # Result of small_expr will be saved to tmp
    def exitSmall_expr(self, ctx: simplerlangParser.Small_exprContext):
        if self.ignoreBlockDepth == 0:
            # SINGLE VALUE
            if ctx.getChildCount() == 1:
                if isinstance(ctx.children[0], simplerlangParser.VarContext):
                    # Single NAME
                    if ctx.children[0].NAME() is not None:
                        self.tmp = self.variableNamesMap[ctx.children[0].NAME().__str__()]

                    # Single Array
                    elif ctx.children[0].array() is not None:
                        self.tmp = eval(ctx.children[0].getText())

                    # Single constant
                    else:
                        self.tmp = ctx.children[0].getText()

            # Binop
            if ctx.getChildCount() == 3: # TODO: Check if ctx contains children: var, bin_op, expr (all contexts) instead of counting them. Current implementation gets messed up if condition has parenthesis.
                if isinstance(ctx.children[0], simplerlangParser.VarContext):
                    # NAME and binop
                    if ctx.children[0].NAME() is not None:
                        secondTmp = self.variableNamesMap[ctx.children[0].NAME().__str__()]
                        self.tmp = eval(str(secondTmp) + " " + ctx.bin_opr().getText() + " " + str(self.tmp))

                    # TODO: Add array addition

                    # Constant and binop
                    else:
                        self.tmp = eval(ctx.children[0].getText() + " " + ctx.bin_opr().getText() + " " + str(self.tmp))
        else:
            # print("Block ignored")
            pass

    # After evaluating condition, mark the evaluation of If_block
    def exitCondition(self, ctx: simplerlangParser.ConditionContext):
        if isinstance(ctx.parentCtx, simplerlangParser.If_blockContext):
            if self.tmp:
                self.If_block2EvaluationMap[ctx.parentCtx] = True
            else:
                self.If_block2EvaluationMap[ctx.parentCtx] = False

    def exitShow(self, ctx: simplerlangParser.ShowContext):
        if self.ignoreBlockDepth == 0:
            print(self.tmp)

    # Set global flag if entering a block that should be ignored
    def enterCode_block(self, ctx: simplerlangParser.Code_blockContext):
        if self.If_block2EvaluationMap[ctx.parentCtx]:
            pass
        else:
            # Condition tied to this block is False. Ignore this block.
            self.ignoreBlockDepth += 1

    # If leaving block of ignored code then stop ignoring code
    def exitCode_block(self, ctx: simplerlangParser.Code_blockContext):
        if not self.If_block2EvaluationMap[ctx.parentCtx]:
            # Ignored block stopped being processed.
            self.ignoreBlockDepth -= 1
