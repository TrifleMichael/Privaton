from gen.ContextTree import ContextTree, NodeType
from gen.privetonParser import privetonParser
from gen.privetonVisitor import privetonVisitor


class privetonVisitorExtended(privetonVisitor):

    def __init__(self):
        self.contextTree = ContextTree()

    def visitReturn_call(self, ctx:privetonParser.Return_callContext):
        if not self.contextTree.isCurrentlyBlocked():
            # Evaluate value of return
            self.visitChildren(ctx)
            # Find value of the evaluation
            returnEvaluation = self.contextTree.searchExpression(ctx.expr())
            # Find the function call to be assigned value
            functionCallCtx = self.contextTree.findCurrentFunctionCallCtx()
            # Set the value of the call to the evaluation
            self.contextTree.functionCallEvaluations[functionCallCtx] = returnEvaluation
            # TODO: Block further processing of the call

    def visitFun_def(self, ctx:privetonParser.Fun_defContext):
        self.contextTree.addFunctionNode(ctx)

    def visitFunc_call(self, ctx:privetonParser.Func_callContext):
        if not self.contextTree.isCurrentlyBlocked():
            # Find the function
            funcNode = self.contextTree.searchFunctionNode(ctx.NAME().__str__())
            # Check for proper number of arguments
            if len(ctx.var()) != len(funcNode.funcArgs):
                raise Exception("Expecting "+str(len(funcNode.funcArgs))+" arguments for function "+ctx.NAME().__str__()+" got "+str(len(ctx.var()))+" instead.")
            # Set the arguments from call as values in the function argument map
            for varArg, argName in zip(ctx.var(), funcNode.funcArgs):
                try:
                    funcNode.funcArgs[argName] = self.castVarToProperType(varArg)
                except:
                    raise Exception("Argument could not be evaluated in call: "+str(ctx.getText()))

            # Run the function
            self.contextTree.enterAndAddChildToCurrentNode(ctx, NodeType.FUNCTION_CALL)
            # self.contextTree.enterAndAddChildToCurrentNode(funcNode.ctx, NodeType.FUNCTION_CALL)
            self.visitChildren(funcNode.ctx)
            # Leave the function context
            self.contextTree.leaveChildNode()

    def visitElse_block(self, ctx:privetonParser.Else_blockContext):
        if not self.contextTree.isCurrentlyBlocked():
            self.contextTree.enterAndAddChildToCurrentNode(ctx, NodeType.ELSE_BLOCK)
            self.visitChildren(ctx)
            self.contextTree.leaveChildNode()

    def visitWhile_block(self, ctx:privetonParser.While_blockContext):
        if not self.contextTree.isCurrentlyBlocked():
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
        if not self.contextTree.isCurrentlyBlocked():
            self.contextTree.enterAndAddChildToCurrentNode(ctx, NodeType.IF_BLOCK)
            self.visitChildren(ctx)
            self.contextTree.leaveChildNode()

    def visitCondition(self, ctx: privetonParser.ConditionContext):
        if not self.contextTree.isCurrentlyBlocked():
            self.visitChildren(ctx)
            if self.contextTree.currentNode.conditionNode is None:
                self.contextTree.addConditionNodeToCurrentNode(ctx)
            evaluatedCondition = eval(str(self.contextTree.searchExpression(ctx.expr())))
            self.contextTree.currentNode.blocked = not evaluatedCondition

    def visitShow(self, ctx: privetonParser.ShowContext):
        if not self.contextTree.isCurrentlyBlocked():
            self.visitChildren(ctx)
            print(self.contextTree.searchExpression(ctx.expr()))

    def visitLet(self, ctx:privetonParser.LetContext):
        if not self.contextTree.isCurrentlyBlocked():
            self.visitChildren(ctx)
            if ctx.NAME() is not None:
                self.contextTree.addVariable(ctx.NAME().__str__(), self.contextTree.searchExpression(ctx.expr()))
            if ctx.outer_name() is not None:
                self.contextTree.modifyOuterVariable(ctx.outer_name().NAME().__str__(), self.contextTree.searchExpression(ctx.expr()))

    def visitExpr(self, ctx: privetonParser.ExprContext):
        if not self.contextTree.isCurrentlyBlocked():
            self.visitChildren(ctx)
            self.contextTree.addChildToCurrentNode(ctx, NodeType.OTHER)

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
                # Internal variable
                if ctx.var().NAME() is not None:
                    self.contextTree.addExpression(ctx, self.contextTree.searchVariable(ctx.var().getText()))
                # External variable
                elif ctx.var().outer_name() is not None:
                    self.contextTree.addExpression(ctx, self.contextTree.searchOuterVariable(ctx.var().outer_name().NAME().getText()))
                # Actually a constant. The names aren't perfect...
                else:
                    self.contextTree.addExpression(ctx, self.castVarToProperType(ctx.var()))
            else:
                print("INCORRECT EXPRESSION:", ctx.getText())

            # self.environment.evaluations.append(self.contextTree.searchExpression(ctx))

    def castVarToProperType(self, ctx):
        if ctx.INT() is not None:
            return int(ctx.getText())
        elif ctx.FLOAT() is not None:
            return float(ctx.getText())
        elif ctx.STRING() is not None:
            return ctx.getText()[1:-1]  # Removing the quotations from input
        elif ctx.LOGIC() is not None:
            return ctx.getText() == "True"
        elif ctx.func_call() is not None:
            if ctx.func_call() in self.contextTree.functionCallEvaluations:
                return self.contextTree.functionCallEvaluations[ctx.func_call()]
            else:
                return None
        else:
            raise Exception("Internal error: No cast found for "+str(ctx.getText()))
