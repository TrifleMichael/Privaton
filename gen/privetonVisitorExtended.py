from gen.ContextTree import ContextTree, NodeType
from gen.privetonParser import privetonParser
from gen.privetonVisitor import privetonVisitor


class privetonVisitorExtended(privetonVisitor):

    def __init__(self):
        self.contextTree = ContextTree()

    def visitLet_object_variable(self, ctx:privetonParser.Let_object_variableContext):
        if not self.contextTree.isCurrentlyBlocked():
            # Visit the expression to evaluate it
            self.visitChildren(ctx)
            # Get the object node
            objectNode = self.contextTree.findObjectNode(ctx.NAME(0).getText())
            # Get the new value of the variable
            newValue = self.contextTree.searchExpression(ctx.expr())
            # Change the value of the variable within the object base node
            variableName = ctx.NAME(1).getText()
            if variableName in objectNode.variable_names_map:
                objectNode.variable_names_map[variableName] = newValue
            else:
                print("Error,", variableName, "is not declared in object:", ctx.NAME(0).getText())
                exit()

    def visitLet_object(self, ctx:privetonParser.Let_objectContext):
        if not self.contextTree.isCurrentlyBlocked():
            # Save the name of currently created object
            self.contextTree.letObjectLastName = ctx.NAME().getText()
            self.visitChildren(ctx)
            # The actual assignment is performed in object_declaration

    def visitObject_declaration(self, ctx:privetonParser.Object_declarationContext):
        if not self.contextTree.isCurrentlyBlocked():
            # Find class declaration
            classCtx = self.contextTree.findClassContext(ctx.NAME().getText())
            # Enter class declaration, with object initialization context
            self.contextTree.enterAndAddChildToCurrentNode(ctx, NodeType.OBJECT)
            # Save object name and reference in local dictionary. Use the name saved in visitLet_object().
            parent = self.contextTree.currentNode.parent
            parent.objectNodesMap[self.contextTree.letObjectLastName] = self.contextTree.currentNode
            # Run child nodes in class declaration
            self.visitChildren(classCtx)
            # Exit object initialization context
            self.contextTree.leaveChildNode()

    def visitClass_def(self, ctx:privetonParser.Class_defContext):
        # Add class context to global class dictionary
        self.contextTree.classContexts[ctx.NAME().getText()] = ctx

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
            # Block the execution of code until function call finishes
            self.contextTree.blockedByReturn = True

    def visitFun_def(self, ctx:privetonParser.Fun_defContext):
        self.contextTree.addFunctionNode(ctx)

    def visitFunc_call(self, ctx:privetonParser.Func_callContext):
        if not self.contextTree.isCurrentlyBlocked():
            # Evaluate expressions
            self.visitChildren(ctx)
            # Find the function definition node
            funcNode = self.contextTree.searchFunctionNode(ctx.NAME().__str__())
            # Enter function call node
            self.contextTree.enterAndAddChildToCurrentNode(ctx, NodeType.FUNCTION_CALL)
            # Check for proper number of arguments
            if len(ctx.expr()) != len(funcNode.funcArgs):
                print("Expecting "+str(len(funcNode.funcArgs))+" arguments for function "+ctx.NAME().__str__()+" got "+str(len(ctx.expr()))+" instead.")
                exit()
            # Set the arguments from call as values in the function argument map
            for exprArg, argName in zip(ctx.expr(), funcNode.funcArgs):
                try:
                    self.contextTree.currentNode.funcArgs[argName] = self.contextTree.searchExpression(exprArg)
                except:
                    print("Argument could not be evaluated in function call: "+str(ctx.getText()))
                    exit()

            # Run the function
            self.visitChildren(funcNode.ctx)
            # Unblock after the function returned
            self.contextTree.blockedByReturn = False
            # Leave the function context
            self.contextTree.leaveChildNode()

    def visitObject_function_call(self, ctx:privetonParser.Object_function_callContext):
        if not self.contextTree.isCurrentlyBlocked():
            # Evaluate expressions
            self.visitChildren(ctx)
            # Find node of the object
            objectNode = self.contextTree.findObjectNode(ctx.NAME(0).getText())
            # Find the function within the object
            funcNode = objectNode.functionNodes[ctx.NAME(1).__str__()]

            # If the function is private allow it to run only if operating in the context of the same object
            if funcNode.private:
                lastObjectNode = self.contextTree.lastObjectNode()
                if lastObjectNode is None:
                    print("Private function", ctx.NAME(1).getText(), "cannot be ran in this context.")
                    exit()
                if lastObjectNode.ctx.NAME().getText() != objectNode.ctx.NAME().getText():
                    print("Private function", ctx.NAME(1).getText(), "cannot be ran in this context.")
                    exit()

            # Enter the object node
            self.contextTree.reenterChildNode(objectNode)
            # Enter function call node
            self.contextTree.enterAndAddChildToCurrentNode(ctx, NodeType.OBJECT_FUNCTION_CALL)
            # Check for proper number of arguments
            if len(ctx.expr()) != len(funcNode.funcArgs):
                print("Expecting "+str(len(funcNode.funcArgs))+" arguments for function "+ctx.NAME().__str__()+" got "+str(len(ctx.expr()))+" instead.")
                exit()

            # Set the arguments from call as values in the function argument map
            for exprArg, argName in zip(ctx.expr(), funcNode.funcArgs):
                try:
                    self.contextTree.currentNode.funcArgs[argName] = self.contextTree.searchExpression(exprArg)
                except:
                    print("Argument", exprArg.getText(), "could not be evaluated in method call: "+str(ctx.getText()))
                    exit()

            # Run the function
            self.visitChildren(funcNode.ctx)
            # Unblock after the function returned
            self.contextTree.blockedByReturn = False
            # Leave the function context
            self.contextTree.leaveChildNode()
            # Leave the object context
            self.contextTree.leaveChildNode()

    def visitElse_block(self, ctx:privetonParser.Else_blockContext):
        # Run only if the context is block (original if)
        if self.contextTree.isCurrentlyBlocked():
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
            for expr in ctx.expr():
                print(self.contextTree.searchExpression(expr), end='')
            print()

    def visitLet(self, ctx:privetonParser.LetContext):
        if not self.contextTree.isCurrentlyBlocked():
            self.visitChildren(ctx)
            expressionValue = self.contextTree.searchExpression(ctx.expr())
            if ctx.PRIVATE_TAG() is not None:
                self.contextTree.currentNode.private_variable_names_map[ctx.NAME().__str__()] = expressionValue
                if ctx.outer_name() is not None:
                    print("Cannot create a outer private variable:", ctx.NAME().__str__())
                    exit()
            elif ctx.NAME() is not None:
                self.contextTree.addVariable(ctx.NAME().__str__(), expressionValue)
            elif ctx.outer_name() is not None:
                self.contextTree.modifyOuterVariable(ctx.outer_name().NAME().__str__(), expressionValue)

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
                # Other types handled in caster below
                else:
                    self.contextTree.addExpression(ctx, self.castVarToProperType(ctx.var()))
            else:
                print("INCORRECT EXPRESSION:", ctx.getText())
                exit()

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
            return self.contextTree.findFunctionEvaluation(ctx.func_call())
        elif ctx.object_function_call() is not None:
            return self.contextTree.findFunctionEvaluation(ctx.object_function_call())
        elif ctx.object_variable_call() is not None:
            return self.contextTree.findObjectVariable(ctx.object_variable_call())
        else:
            print("Internal error: No cast found for "+str(ctx.getText()))
            exit()
