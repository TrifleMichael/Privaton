from enum import Enum

class NodeType(Enum):
    LOOP = 1
    IF_BLOCK = 2
    OTHER = 3
    ELSE_BLOCK = 4

class ContextTree:
    def __init__(self):
        self.nodes = [ContextTreeNode(None, None, NodeType.OTHER)]
        self.currentNode = self.nodes[0]
        self.depth = 0  # used for debug

    def enterAndAddChildToCurrentNode(self, ctx, type):
        self.currentNode.children.append(ContextTreeNode(ctx, self.currentNode, type))
        self.currentNode = self.currentNode.children[-1]
        self.depth += 1

    def addChildToCurrentNode(self, ctx, type):
        self.currentNode.children.append(ContextTreeNode(ctx, self.currentNode, type))

    def leaveChildNode(self):
        self.currentNode = self.currentNode.parent
        self.depth -= 1
        # if self.currentNode.parent is None:
        #     self.nodes = []

    def modifyOuterVariable(self, name, value):
        node = self.currentNode.parent
        while node is not None:
            if name in node.variable_names_map:
                node.variable_names_map[name] = value
                return
            node = node.parent
        raise Exception("No variable "+str(name)+" found in outer scope.")
        # self.currentNode.addVariable(name, value)

    def addVariable(self, name, value):
        self.currentNode.variable_names_map[name] = value

    def addExpression(self, ctx, value):
        self.currentNode.addExpression(ctx, value)

    # def addCondition(self, ctx, value):
    #     self.currentNode.conditionContext = ctx
    #     self.currentNode.conditionValue = value
    #
    # def getConditionValue(self):
    #     if self.currentNode.conditionValue is not None and self.currentNode.conditionContext is not None:
    #         return self.currentNode.conditionValue
    #
    # def startConditionEvaluation(self):
    #     self.currentNode.evaluating = True
    #
    # def endConditionEvaluation(self):
    #     self.currentNode.evaluating = False
    #
    def searchVariable(self, variableName):
        if variableName in self.currentNode.variable_names_map:
            return self.currentNode.variable_names_map[variableName]
        raise Exception("VARIABLE WITH NAME " + str(variableName) + " NOT FOUND")

    def searchOuterVariable(self, variableName):
        tempNode = self.currentNode.parent
        while tempNode is not None:
            if variableName in tempNode.variable_names_map:
                return tempNode.variable_names_map[variableName]
            tempNode = tempNode.parent
        raise Exception("VARIABLE WITH NAME " + str(variableName) + " NOT FOUND IN OUTER SCOPE")

    def searchExpression(self, expression):
        tempNode = self.currentNode
        while tempNode is not None:
            if expression in tempNode.expressions_value_map:
                return tempNode.expressions_value_map[expression]
            tempNode = tempNode.parent
        raise Exception("EXPRESSION: " + str(expression.getText()) + " NOT FOUND")

    def addConditionNodeToCurrentNode(self, conditionCtx):
        self.currentNode.conditionNode = ContextTreeNode(conditionCtx, self.currentNode, NodeType.OTHER)

# Only IF and WHILE blocks can have children
class ContextTreeNode:
    def __init__(self, ctx, parent, type):
        self.ctx = ctx
        self.parent = parent
        self.type = type
        self.children = []

    #     self.parent = parent
    #     self.children = []
    #     self.ctx = ctx
    #     self.entering = entering
    #
        self.expressions_value_map = {}
        self.variable_names_map = {}

        self.conditionNode = None
    #     self.conditionReevaluationSteps = []
    #
    #     self.repeating = False
    #     self.reevaluating = False
    #     self.evaluating = True
    #
        self.blocked = False

    def addVariable(self, name, value):
        self.variable_names_map[name] = value

    def addExpression(self, ctx, value):
        self.expressions_value_map[ctx] = value

    def blockNode(self):
        self.blocked = True

    def unblockNode(self):
        self.blocked = False

    def isBlocked(self):
        return self.blocked
