from gen.ContextTree import ContextTree, NodeType
from gen.privetonParser import privetonParser
from gen.privetonVisitor import privetonVisitor


class privetonVisitorExtended(privetonVisitor):

    def __init__(self):
        self.contextTree = ContextTree()

    def visitFun_def(self, ctx:privetonParser.Fun_defContext):
        self.visitChildren(ctx)

    def visitElse_block(self, ctx:privetonParser.Else_blockContext):
        if self.contextTree.currentNode.isBlocked():
            self.contextTree.enterAndAddChildToCurrentNode(ctx, NodeType.ELSE_BLOCK)
            self.visitChildren(ctx)
            self.contextTree.leaveChildNode()

    def visitWhile_block(self, ctx:privetonParser.While_blockContext):
        self.contextTree.enterAndAddChildToCurrentNode(ctx, NodeType.LOOP)
        # Visit each node below that one. Condition will be executed first, and it will define if the rest will execute
        self.visitChildren(ctx)
        # Reevaluate condition after the loop ran
        self.visitCondition(self.contextTree.currentNode.conditionNode.ctx)
        # If condition is still met then run the block again
        while not self.contextTree.currentNode.isBlocked():
            # Run code block
            self.visitCode_block(ctx.code_block())
            # Check condition
            self.visitCondition(self.contextTree.currentNode.conditionNode.ctx)
        self.contextTree.leaveChildNode()

    def visitIf_block(self, ctx:privetonParser.If_blockContext):
        self.contextTree.enterAndAddChildToCurrentNode(ctx, NodeType.IF_BLOCK)
        self.visitChildren(ctx)
        self.contextTree.leaveChildNode()

    def visitCondition(self, ctx: privetonParser.ConditionContext):
        self.visitChildren(ctx)
        if self.contextTree.currentNode.conditionNode is None:
            self.contextTree.addConditionNodeToCurrentNode(ctx)
        evaluatedCondition = eval(str(self.contextTree.searchExpression(ctx.expr())))
        self.contextTree.currentNode.blocked = not evaluatedCondition

    def visitShow(self, ctx: privetonParser.ShowContext):
        self.visitChildren(ctx)
        if not self.contextTree.currentNode.isBlocked():
            print(self.contextTree.searchExpression(ctx.expr()))

    def visitLet(self, ctx:privetonParser.LetContext):
        self.visitChildren(ctx)
        if not self.contextTree.currentNode.isBlocked():
            if ctx.NAME() is not None:
                self.contextTree.addVariable(ctx.NAME().__str__(), self.contextTree.searchExpression(ctx.expr()))
            if ctx.outer_name() is not None:
                self.contextTree.modifyOuterVariable(ctx.outer_name().NAME().__str__(), self.contextTree.searchExpression(ctx.expr()))

    def visitExpr(self, ctx: privetonParser.ExprContext):
        self.visitChildren(ctx)
        self.contextTree.addChildToCurrentNode(ctx, NodeType.OTHER)

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
                elif ctx.var().outer_name() is not None:
                    self.contextTree.addExpression(ctx, self.contextTree.searchOuterVariable(ctx.var().outer_name().NAME().getText()))
                else:
                    self.contextTree.addExpression(ctx, self.castVarToProperType(ctx.var()))
            else:
                print("INCORRECT EXPRESSION:", ctx.getText())

            # self.environment.evaluations.append(self.contextTree.searchExpression(ctx))

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
