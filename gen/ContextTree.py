from enum import Enum

from gen.privetonParser import privetonParser


class NodeType(Enum):
    LOOP = 1
    IF_BLOCK = 2
    OTHER = 3
    ELSE_BLOCK = 4
    FUNCTION = 5
    FUNCTION_CALL = 6

class ContextTree:
    def __init__(self):
        self.nodes = [ContextTreeNode(None, None, NodeType.OTHER)]
        self.functionNodes = {}
        self.functionCallEvaluations = {}
        self.blockedByReturn = False
        self.currentNode = self.nodes[0]
        self.depth = 0  # used for debug

    def isCurrentlyBlocked(self):
        return self.blockedByReturn or self.currentNode.isBlocked()

    def findCurrentFunctionCallCtx(self):
        node = self.currentNode
        while node is not None and node.type is not NodeType.FUNCTION_CALL:
            node = node.parent
        if node is None:
            raise Exception("Internal error, resolving function call failed.")
        else:
            return node.ctx

    def addFunctionNode(self, ctx:privetonParser.Fun_defContext):
        funcName = ctx.NAME().__str__()
        # Saving function in a global map
        self.functionNodes[funcName] = ContextTreeNode(ctx, None, NodeType.FUNCTION)
        # Saving function argument names with None values
        for varArg in ctx.var():
            self.functionNodes[funcName].funcArgs[varArg.getText()] = None

    def searchFunctionNode(self, funcName):
        if funcName in self.functionNodes:
            return self.functionNodes[funcName]
        raise Exception("Function with name "+str(funcName)+" does not exit.")

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

    def searchVariable(self, variableName):
        # Search in function context, if currently in a function
        if self.currentNode.type == NodeType.FUNCTION_CALL:
            # Find the function that is being ran, through name stored in the call that is being executed
            funcNode = self.functionNodes[self.currentNode.ctx.NAME().__str__()]
            # Check if function contains the name that is used, if so return the value.
            if variableName in funcNode.funcArgs:
                return funcNode.funcArgs[variableName]
        # Search in local context
        if variableName in self.currentNode.variable_names_map:
            return self.currentNode.variable_names_map[variableName]
        raise Exception("VARIABLE WITH NAME " + str(variableName) + " NOT FOUND")

    def searchOuterVariable(self, variableName):
        tempNode = self.currentNode.parent
        while tempNode is not None:
            # Check in normal variables
            if variableName in tempNode.variable_names_map:
                return tempNode.variable_names_map[variableName]
            # Check in function call variables
            if tempNode.type == NodeType.FUNCTION_CALL:
                print("SEARCHING FOR", variableName, "IN", tempNode.ctx.getText())
                if variableName in tempNode.funcArgs:
                    return tempNode.funcArgs[variableName]
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

        self.expressions_value_map = {}
        self.variable_names_map = {}

        self.conditionNode = None

        self.blocked = False

        self.funcArgs = {}

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
