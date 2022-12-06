import privetonParser
from gen.privetonListener import privetonListener
from gen.privetonParser import privetonParser
from gen.Environment import Environment


class PrivetonListenerExtended(privetonListener):
    def __init__(self):
        self.environment = Environment()

    # How many blocks up, including the one analyzed, will be ignored (used by nested ifs)

    def exitLet(self, ctx: privetonParser.LetContext):
        if self.environment.ignore_block_depth == 0:
            self.environment.variable_names_map[ctx.NAME().__str__()] = self.environment.expressions_value_map[
                ctx.large_expr()]

    def exitLarge_expr(self, ctx: privetonParser.Large_exprContext):
        if self.environment.ignore_block_depth == 0:
            if ctx.large_expr() is not None:
                self.environment.expressions_value_map[ctx] = eval(
                    str(self.environment.expressions_value_map[
                            ctx.small_expr()]) + " " + ctx.bin_opr().getText() + " " + str(
                        self.environment.expressions_value_map[ctx.large_expr()]))
            else:
                self.environment.expressions_value_map[ctx] = self.environment.expressions_value_map[ctx.small_expr()]
        self.environment.evaluations.append(self.environment.expressions_value_map[ctx])

    # Result of small_expr will be saved to tmp
    def exitSmall_expr(self, ctx: privetonParser.Small_exprContext):
        if self.environment.ignore_block_depth == 0:
            # SINGLE VALUE
            if ctx.bin_opr() is None:

                if isinstance(ctx.var(), privetonParser.VarContext):
                    # Single NAME
                    if ctx.var().NAME() is not None:
                        tmp = self.environment.variable_names_map[ctx.var().NAME().__str__()]

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
                        secondTmp = self.environment.variable_names_map[ctx.var().NAME().__str__()]
                        tmp = eval(str(secondTmp) + " " + ctx.bin_opr().getText() + " " + str(
                            self.environment.expressions_value_map[ctx.small_expr()]))

                    # TODO: Add array addition

                    # Constant and binop
                    else:
                        tmp = eval(ctx.var().getText() + " " + ctx.bin_opr().getText() + " " + str(
                            self.environment.expressions_value_map[ctx.small_expr()]))
            self.environment.expressions_value_map[ctx] = tmp
        else:
            # print("Block ignored")
            pass

    # After evaluating condition, mark the evaluation of If_block
    def exitCondition(self, ctx: privetonParser.ConditionContext):
        if isinstance(ctx.parentCtx, privetonParser.If_blockContext):
            if eval(str(
                    self.environment.expressions_value_map[ctx.large_expr()])):  # This way for every type of self.tmpL
                self.environment.if_block_to_evaluation_map[ctx.parentCtx] = True
            else:
                self.environment.if_block_to_evaluation_map[ctx.parentCtx] = False

    def exitShow(self, ctx: privetonParser.ShowContext):
        if self.environment.ignore_block_depth == 0:
            print(self.environment.expressions_value_map[ctx.large_expr()])

    # Set global flag if entering a block that should be ignored
    def enterCode_block(self, ctx: privetonParser.Code_blockContext):
        if isinstance(ctx.parentCtx, privetonParser.If_blockContext):
            if self.environment.if_block_to_evaluation_map[ctx.parentCtx]:
                pass
            else:
                # Condition tied to this block is False. Ignore this block.
                self.environment.ignore_block_depth += 1

    # If leaving block of ignored code then stop ignoring code
    def exitCode_block(self, ctx: privetonParser.Code_blockContext):
        if isinstance(ctx.parentCtx, privetonParser.If_blockContext):
            if not self.environment.if_block_to_evaluation_map[ctx.parentCtx]:
                # Ignored block stopped being processed.
                self.environment.ignore_block_depth -= 1

    def enterElse_block(self, ctx: privetonParser.Else_blockContext):
        if self.environment.if_block_to_evaluation_map[ctx.parentCtx]:
            # Evaluation of parent 'if' succeeded so the next code block gets ignored
            self.environment.ignore_block_depth += 1

    def exitElse_block(self, ctx: privetonParser.Else_blockContext):
        if self.environment.if_block_to_evaluation_map[ctx.parentCtx]:
            # Evaluation of parent 'if' succeeded, and code block got processed, so time to restore previous block depth
            self.environment.ignore_block_depth -= 1

    # Clean expression to value map after leaving statement
    def exitStatement(self, ctx: privetonParser.StatementContext):
        self.environment.expressions_value_map = {}
        pass
