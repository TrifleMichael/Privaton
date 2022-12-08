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
            string = ""
            for i, smallExpr in enumerate(ctx.small_expr()):
                string += str(self.environment.expressions_value_map[smallExpr])
                if i != len(ctx.bin_opr()):
                    string += ctx.bin_opr(i).getText()
            self.environment.expressions_value_map[ctx] = eval(string)

        self.environment.evaluations.append(self.environment.expressions_value_map[ctx])

    # Result of small_expr will be saved to tmp
    def exitSmall_expr(self, ctx: privetonParser.Small_exprContext):
        if self.environment.ignore_block_depth == 0:
            # SINGLE VALUE
            if ctx.var() is None:
                string = ""
                for i, smallExpr in enumerate(ctx.small_expr()):
                    string += str(self.environment.expressions_value_map[smallExpr])
                    if i != len(ctx.bin_opr()):
                        string += ctx.bin_opr(i).getText()
                self.environment.expressions_value_map[ctx] = eval(string)
            else:
                if ctx.var().NAME() is not None:
                    self.environment.expressions_value_map[ctx] = self.environment.variable_names_map[ctx.var().getText()]
                else:
                    self.environment.expressions_value_map[ctx] = ctx.var().getText()
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
