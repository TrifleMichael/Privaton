import privetonParser
from gen.ContextTree import ContextTree
from gen.privetonListener import privetonListener
from gen.privetonParser import privetonParser
from gen.Environment import Environment

# TODO: Add possibility to modify function variables when in deeper contexts
class PrivetonListenerExtended(privetonListener):
    def __init__(self):
        self.environment = Environment()
        self.contextTree = ContextTree()

    def reevaluateCondition(self):
        self.contextTree.currentNode.reevaluating = True
        for ctx, entering in self.contextTree.currentNode.conditionReevaluationSteps:
            if entering:
                ctx.enterRule(self)
            else:
                ctx.exitRule(self)
        self.contextTree.currentNode.reevaluating = False

    def enterWhile_block(self, ctx:privetonParser.While_blockContext):
        self.contextTree.enterAndAddChildToCurrentNode(ctx, True)

    def exitWhile_block(self, ctx:privetonParser.While_blockContext):
        # Reevaluate condition, if still True then repeat loop
        self.contextTree.currentNode.repeating = True
        self.reevaluateCondition()
        while not self.contextTree.currentNode.isBlocked():
            for child in self.contextTree.currentNode.children:
                entry = child.ctx
                if child.entering:
                    entry.enterRule(self)
                else:
                    entry.exitRule(self)
            self.reevaluateCondition()

        self.contextTree.currentNode.repeating = False
        self.contextTree.leaveChildNode()
        if not self.contextTree.currentNode.repeating:
            self.contextTree.addChildToCurrentNode(ctx, False)


    def exitLet(self, ctx: privetonParser.LetContext):
        self.contextTree.addChildToCurrentNode(ctx, False)
        if not self.contextTree.currentNode.isBlocked():
            self.contextTree.addVariable(ctx.NAME().__str__(), self.contextTree.searchExpression(ctx.expr()))

    # Result of small_expr will be saved to tmp
    def exitExpr(self, ctx: privetonParser.ExprContext):
        if self.contextTree.currentNode.evaluating:
            self.contextTree.currentNode.conditionReevaluationSteps.append([ctx, False])  # Context - Entering
        self.contextTree.addChildToCurrentNode(ctx, False)

        if not self.contextTree.currentNode.isBlocked():
            # TWO EXPR
            if ctx.expr(0) is not None and ctx.expr(1) is not None:
                string = ""
                string += str(self.contextTree.searchExpression(ctx.expr(0)))
                if ctx.priority_opr() is not None:
                    string += ctx.priority_opr().getText()
                else:
                    string += ctx.non_priority_opr().getText()
                string += str(self.contextTree.searchExpression(ctx.expr(1)))
                self.contextTree.addExpression(ctx, eval(string))
            # ONE EXPR
            elif ctx.expr(0) is not None and ctx.expr(1) is None and ctx.un_opr() is None:
                self.contextTree.addExpression(ctx, self.contextTree.searchExpression(ctx.expr(0)))
            # UNARY OPR
            elif ctx.un_opr() is not None:
                temp = eval(ctx.un_opr().getText() + str(self.contextTree.searchExpression(ctx.expr(0))))
                self.contextTree.addExpression(ctx, temp)
            # ONE VAR
            elif ctx.var() is not None:
                if ctx.var().NAME() is not None:
                    self.contextTree.addExpression(ctx, self.contextTree.searchVariable(ctx.var().getText()))
                else:
                    self.contextTree.addExpression(ctx, self.castVarToProperType(ctx.var()))
            else:
                print("INCORRECT EXPRESSION:", ctx.getText())

            self.environment.evaluations.append(self.contextTree.searchExpression(ctx))
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
        self.contextTree.startConditionEvaluation()

    # After evaluating condition, mark the evaluation of If_block
    def exitCondition(self, ctx: privetonParser.ConditionContext):
        if self.contextTree.currentNode.evaluating:
            self.contextTree.currentNode.conditionReevaluationSteps.append([ctx, False])  # Context - Entering

        self.contextTree.currentNode.conditionContext = ctx
        if eval(str(self.contextTree.searchExpression(ctx.expr()))):  # This way for every type of self.tmpL
            self.contextTree.currentNode.unblockNode()
        else:
            self.contextTree.currentNode.blockNode()
        self.contextTree.endConditionEvaluation()

    def exitShow(self, ctx: privetonParser.ShowContext):
        self.contextTree.addChildToCurrentNode(ctx, False)

        if not self.contextTree.currentNode.isBlocked():
            print(self.contextTree.searchExpression(ctx.expr()))

    def enterIf_block(self, ctx:privetonParser.If_blockContext):
        self.contextTree.enterAndAddChildToCurrentNode(ctx, True)

    def exitIf_block(self, ctx:privetonParser.If_blockContext):
        self.contextTree.leaveChildNode()

    # Set global flag if entering a block that should be ignored
    def enterCode_block(self, ctx: privetonParser.Code_blockContext):
        self.contextTree.addChildToCurrentNode(ctx, True)

    # If leaving block of ignored code then stop ignoring code
    def exitCode_block(self, ctx: privetonParser.Code_blockContext):
        self.contextTree.addChildToCurrentNode(ctx, False)

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
        self.environment.expressions_value_map = {}
