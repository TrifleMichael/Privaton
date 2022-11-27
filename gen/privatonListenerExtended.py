import privetonParser
from gen.privetonListener import privetonListener
from gen.privetonParser import privetonParser


class PrivetonListenerExtended(privetonListener):
    variableNamesMap = {}
    If_block2EvaluationMap = {}
    blockIgnoreMap = {}
    exprValMap = {}
    ignoreBlockDepth = 0  # How many blocks up, including the one analyzed, will be ignored (used by nested ifs)

    def exitLet(self, ctx: privetonParser.LetContext):
        if self.ignoreBlockDepth == 0:
            self.variableNamesMap[ctx.NAME().__str__()] = self.exprValMap[ctx.large_expr()]

    def exitLarge_expr(self, ctx:privetonParser.Large_exprContext):
        if self.ignoreBlockDepth == 0:
            if ctx.large_expr() is not None:
                self.exprValMap[ctx] = eval(str(self.exprValMap[ctx.small_expr()]) + " " + ctx.bin_opr().getText() + " " + str(self.exprValMap[ctx.large_expr()]))
            else:
                self.exprValMap[ctx] = self.exprValMap[ctx.small_expr()]

    # Result of small_expr will be saved to tmp
    def exitSmall_expr(self, ctx: privetonParser.Small_exprContext):
        if self.ignoreBlockDepth == 0:
            # SINGLE VALUE
            if ctx.bin_opr() is None:

                if isinstance(ctx.var(), privetonParser.VarContext):
                    # Single NAME
                    if ctx.var().NAME() is not None:
                        tmp = self.variableNamesMap[ctx.var().NAME().__str__()]

                    # Single Array
                    elif ctx.var().array() is not None:
                        tmp = eval(ctx.var().getText())

                    elif ctx.var().STRING() is not None:
                        tmp = ctx.var().STRING().getText()[1:-1]

                    # Single constant
                    else:
                        tmp = ctx.var().getText()

            # Binop
            if ctx.bin_opr() is not None:
                if isinstance(ctx.var(), privetonParser.VarContext):
                    # NAME and binop
                    if ctx.var().NAME() is not None:
                        secondTmp = self.variableNamesMap[ctx.var().NAME().__str__()]
                        tmp = eval(str(secondTmp) + " " + ctx.bin_opr().getText() + " " + str(self.exprValMap[ctx.small_expr()]))

                    # TODO: Add array addition

                    # Constant and binop
                    else:
                        tmp = eval(ctx.var().getText() + " " + ctx.bin_opr().getText() + " " + str(self.exprValMap[ctx.small_expr()]))

            self.exprValMap[ctx] = tmp
        else:
            # print("Block ignored")
            pass

    # After evaluating condition, mark the evaluation of If_block
    def exitCondition(self, ctx: privetonParser.ConditionContext):
        if isinstance(ctx.parentCtx, privetonParser.If_blockContext):
            if eval(str(self.exprValMap[ctx.large_expr()])):  # This way for every type of self.tmpL
                self.If_block2EvaluationMap[ctx.parentCtx] = True
            else:
                self.If_block2EvaluationMap[ctx.parentCtx] = False

    def exitShow(self, ctx: privetonParser.ShowContext):
        if self.ignoreBlockDepth == 0:
            print(self.exprValMap[ctx.large_expr()])

    # Set global flag if entering a block that should be ignored
    def enterCode_block(self, ctx: privetonParser.Code_blockContext):
        if isinstance(ctx.parentCtx, privetonParser.If_blockContext):
            if self.If_block2EvaluationMap[ctx.parentCtx]:
                pass
            else:
                # Condition tied to this block is False. Ignore this block.
                self.ignoreBlockDepth += 1

    # If leaving block of ignored code then stop ignoring code
    def exitCode_block(self, ctx: privetonParser.Code_blockContext):
        if isinstance(ctx.parentCtx, privetonParser.If_blockContext):
            if not self.If_block2EvaluationMap[ctx.parentCtx]:
                # Ignored block stopped being processed.
                self.ignoreBlockDepth -= 1

    def enterElse_block(self, ctx:privetonParser.Else_blockContext):
        if self.If_block2EvaluationMap[ctx.parentCtx]:
            # Evaluation of parent 'if' succeeded so the next code block gets ignored
            self.ignoreBlockDepth += 1

    def exitElse_block(self, ctx:privetonParser.Else_blockContext):
        if self.If_block2EvaluationMap[ctx.parentCtx]:
            # Evaluation of parent 'if' succeeded, and code block got processed, so time to restore previous block depth
            self.ignoreBlockDepth -= 1

    # Clean expression to value map after leaving statement
    def exitStatement(self, ctx:privetonParser.StatementContext):
        self.exprValMap = {}