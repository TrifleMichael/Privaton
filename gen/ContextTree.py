class ContextTree:
    def __init__(self):
        self.nodes = [ContextTreeNode(None, None, None)]
        self.currentNode = self.nodes[0]
        self.depth = 0  # used for debug

    def enterAndAddChildToCurrentNode(self, ctx, entering):
        #  TODO: ADD TO LIST ONLY IF CURRENT NODE IS NOT REPEATING, IN EACH CASE ENTER THE CORRECT NODE
        self.currentNode.children.append(ContextTreeNode(ctx, self.currentNode, entering))
        self.currentNode = self.currentNode.children[-1]
        print("ENTERING", ctx.getText())
        self.depth += 1

    def addChildToCurrentNode(self, ctx, entering):
        if not self.currentNode.repeating:
            self.currentNode.children.append(ContextTreeNode(ctx, self.currentNode, entering))

    def leaveChildNode(self):
        print("LEAVING", self.currentNode.ctx.getText())
        self.currentNode = self.currentNode.parent
        if self.currentNode.parent is None:
            self.nodes = []

        self.depth -= 1

    def addVariable(self, name, value):
        node = self.currentNode
        while node is not None:
            if name in node.variable_names_map:
                node.variable_names_map[name] = value
            node = node.parent
        self.currentNode.addVariable(name, value)

    def addExpression(self, ctx, value):
        self.currentNode.addExpression(ctx, value)

    def addCondition(self, ctx, value):
        self.currentNode.conditionContext = ctx
        self.currentNode.conditionValue = value

    def getConditionValue(self):
        if self.currentNode.conditionValue is not None and self.currentNode.conditionContext is not None:
            return self.currentNode.conditionValue

    def startConditionEvaluation(self):
        self.currentNode.evaluating = True

    def endConditionEvaluation(self):
        self.currentNode.evaluating = False

    def searchVariable(self, variableName):
        tempNode = self.currentNode
        while tempNode is not None:
            if variableName in tempNode.variable_names_map:
                return tempNode.variable_names_map[variableName]
            tempNode = tempNode.parent
        raise Exception("VARIABLE WITH NAME " + str(variableName) + " NOT FOUND")

    def searchExpression(self, expression):
        tempNode = self.currentNode
        while tempNode is not None:
            if expression in tempNode.expressions_value_map:
                return tempNode.expressions_value_map[expression]
            tempNode = tempNode.parent
        raise Exception("EXPRESSION: " + str(expression.getText()) + " NOT FOUND")

# Only IF and WHILE blocks can have children
class ContextTreeNode:
    def __init__(self, ctx, parent, entering):
        self.parent = parent
        self.children = []
        self.ctx = ctx
        self.entering = entering

        self.expressions_value_map = {}
        self.variable_names_map = {}

        self.conditionContext = None
        self.conditionValue = None
        self.conditionReevaluationSteps = []

        self.repeating = False
        self.reevaluating = False
        self.evaluating = True

        self.blocked = False

    def addVariable(self, name, value):
        self.variable_names_map[name] = value

    def addExpression(self, ctx, value):
        self.expressions_value_map[ctx] = value

    def addCondition(self, conditionContex, value):
        self.condition_evaluation_map[conditionContex] = value