import privetonParser
from gen.privetonListener import privetonListener
from gen.privetonParser import privetonParser
from gen.Environment import Environment

class Loop_entry:
    def __init__(self, enter, ctx):
        self.enter = enter
        self.ctx = ctx

class Loop_node: # not yet used
    def __init__(self, ctx, repeating):
        self.ctx = ctx
        self.repeating = repeating

class PrivetonListenerExtended(privetonListener):
    def __init__(self):
        self.environment = Environment()

        self.current_condition = None
        self.reevaluating = False
        self.condition_to_context_arr_dict = {}

        self.loop_to_context_arr_dict = {}
        self.loop_queue = [] # not yet used
        self.repeating = False
        self.current_loop = None

    def addToConditionList(self, ctx, enter=False):
        if self.current_condition is not None:
            self.condition_to_context_arr_dict[self.current_condition].append(Loop_entry(enter, ctx))

    def addToLoopList(self, ctx, enter=False):
        if self.current_loop is not None and not self.repeating:
            self.loop_to_context_arr_dict[self.current_loop].append(Loop_entry(enter, ctx))

    def reevaluateCondition(self, ctx):
        self.reevaluating = True
        for entry in self.condition_to_context_arr_dict[ctx]:
            if entry.enter:
                entry.ctx.enterRule(self)
            else:
                entry.ctx.exitRule(self)
        self.reevaluating = False

    def enterWhile_block(self, ctx:privetonParser.While_blockContext):
        self.current_loop = ctx
        self.loop_to_context_arr_dict[ctx] = []

    def exitWhile_block(self, ctx:privetonParser.While_blockContext):
        # Reevaluate condition, if still True then repeat loop
        self.repeating = True
        self.reevaluateCondition(ctx.condition())
        while self.environment.condition_evaluation_map[ctx.condition()]:
            for entry in self.loop_to_context_arr_dict[self.current_loop]:
                if entry.enter:
                    entry.ctx.enterRule(self)
                else:
                    entry.ctx.exitRule(self)
            self.reevaluateCondition(ctx.condition())
        self.repeating = False
        self.current_loop = None
        del self.loop_to_context_arr_dict[ctx]
        self.environment.ignore_block_depth -= 1  # After condition fails, ignore_depth gets increased

    def exitLet(self, ctx: privetonParser.LetContext):
        if self.environment.ignore_block_depth == 0:
            self.addToLoopList(ctx)
            self.environment.variable_names_map[ctx.NAME().__str__()] = self.environment.expressions_value_map[ctx.expr()]

    # Result of small_expr will be saved to tmp
    def exitExpr(self, ctx: privetonParser.ExprContext):
        if self.environment.ignore_block_depth == 0:
            self.addToConditionList(ctx)
            self.addToLoopList(ctx)
            # TWO EXPR
            if ctx.expr(0) is not None and ctx.expr(1) is not None:
                string = ""
                string += str(self.environment.expressions_value_map[ctx.expr(0)])
                if ctx.priority_opr() is not None:
                    string += ctx.priority_opr().getText()
                else:
                    string += ctx.non_priority_opr().getText()
                string += str(self.environment.expressions_value_map[ctx.expr(1)])
                self.environment.expressions_value_map[ctx] = eval(string)
            # ONE EXPR
            elif ctx.expr(0) is not None and ctx.expr(1) is None and ctx.un_opr() is None:
                self.environment.expressions_value_map[ctx] = self.environment.expressions_value_map[ctx.expr(0)]
            # UNARY OPR
            elif ctx.un_opr() is not None:
                temp = eval(ctx.un_opr().getText() + str(self.environment.expressions_value_map[ctx.expr(0)]))
                self.environment.expressions_value_map[ctx] = temp
            # ONE VAR
            elif ctx.var() is not None:
                if ctx.var().NAME() is not None:
                    self.environment.expressions_value_map[ctx] = self.environment.variable_names_map[ctx.var().getText()]
                else:
                    self.environment.expressions_value_map[ctx] = self.castVarToProperType(ctx.var())
            else:
                print("INCORRECT EXPRESSION:", ctx.getText())

            self.environment.evaluations.append(self.environment.expressions_value_map[ctx])
        else:
            pass

    def castVarToProperType(self, ctx):
        if ctx.INT() is not None:
            return int(ctx.getText())
        if ctx.FLOAT() is not None:
            return float(ctx.getText())
        if ctx.STRING() is not None:
            return ctx.getText()[1:-1]  # Removing the quotations from input
        if ctx.LOGIC() is not None:
            return ctx.getText() == "True"
        if ctx.ARRAY() is not None:
            pass

    def enterCondition(self, ctx:privetonParser.ConditionContext):
        self.current_condition = ctx
        self.condition_to_context_arr_dict[ctx] = []

    # After evaluating condition, mark the evaluation of If_block
    def exitCondition(self, ctx: privetonParser.ConditionContext):
        self.current_condition = None
        if not self.reevaluating:
            self.addToLoopList(ctx)
        if eval(str(
                self.environment.expressions_value_map[ctx.expr()])):  # This way for every type of self.tmpL
            self.environment.condition_evaluation_map[ctx] = True
        else:
            self.environment.condition_evaluation_map[ctx] = False

    def exitShow(self, ctx: privetonParser.ShowContext):
        self.addToLoopList(ctx)
        if self.environment.ignore_block_depth == 0:
            print(self.environment.expressions_value_map[ctx.expr()])

    # Set global flag if entering a block that should be ignored
    def enterCode_block(self, ctx: privetonParser.Code_blockContext):
        self.addToLoopList(ctx, True)
        if self.environment.condition_evaluation_map[ctx.parentCtx.condition()]:
            pass
        else:
            # Condition tied to this block is False. Ignore this block.
            self.environment.ignore_block_depth += 1

    # If leaving block of ignored code then stop ignoring code
    def exitCode_block(self, ctx: privetonParser.Code_blockContext):
        self.addToLoopList(ctx)
        if isinstance(ctx.parentCtx, privetonParser.If_blockContext):
            if not self.environment.condition_evaluation_map[ctx.parentCtx.condition()]:
                # Ignored block stopped being processed.
                self.environment.ignore_block_depth -= 1

    def enterElse_block(self, ctx: privetonParser.Else_blockContext):
        self.addToLoopList(ctx, True)
        if self.environment.condition_evaluation_map[ctx.parentCtx.condition()]:
            # Evaluation of parent 'if' succeeded so the next code block gets ignored
            self.environment.ignore_block_depth += 1

    def exitElse_block(self, ctx: privetonParser.Else_blockContext):
        self.addToLoopList(ctx)
        if self.environment.condition_evaluation_map[ctx.parentCtx.condition()]:
            # Evaluation of parent 'if' succeeded, and code block got processed, so time to restore previous block depth
            self.environment.ignore_block_depth -= 1

    # Clean expression to value map after leaving statement
    def exitStatement(self, ctx: privetonParser.StatementContext):
        if self.environment.ignore_block_depth == 0:
            self.addToLoopList(ctx)
        self.environment.expressions_value_map = {}
