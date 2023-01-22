from enum import Enum

from gen.privetonParser import privetonParser


class NodeType(Enum):
    LOOP = 1
    IF_BLOCK = 2
    BASE = 3
    ELSE_BLOCK = 4
    FUNCTION = 5
    FUNCTION_CALL = 6
    CLASS = 7
    OBJECT = 8
    OTHER = 9
    OBJECT_FUNCTION_CALL = 10

class ContextTree:
    def __init__(self):
        self.nodes = [ContextTreeNode(None, None, NodeType.BASE)]
        self.classContexts = {}
        self.blockedByReturn = False
        self.currentNode = self.nodes[0]
        self.depth = 0  # used for debug
        self.functionCallEvaluations = {}
        self.letObjectLastName = None

    def findObjectNode(self, objectName):
        node = self.currentNode
        while node is not None:
            if objectName in node.objectNodesMap:
                return node.objectNodesMap[objectName]
            node = node.parent
        print("Cannot find object with name:", objectName)
        exit()

    def findObjectVariable(self, ctx:privetonParser.Object_variable_callContext):
        # Find object node
        objectNode = self.findObjectNode(ctx.NAME(0).getText())

        # Find the value of the variable in base variables
        variableName = ctx.NAME(1).getText()
        if variableName in objectNode.variable_names_map:
            return objectNode.variable_names_map[variableName]

        # Check if last object node exists and is the same class as the referenced object
        lastObjectNode = self.lastObjectNode()
        if lastObjectNode is not None and lastObjectNode.ctx.NAME().getText() == objectNode.ctx.NAME().getText():
            # Check for variable in the private variables of the referenced object
            if variableName in objectNode.private_variable_names_map:
                return objectNode.private_variable_names_map[variableName]

        print("Variable", variableName, "not found for object with name", ctx.NAME(0).getText())
        exit()

    def lastObjectNode(self):
        node = self.currentNode
        while node is not None:
            if node.type == NodeType.OBJECT:
                return node
            node = node.parent
        return node

    def findClassContext(self, name):
        if name in self.classContexts:
            return self.classContexts[name]
        else:
            print("Cannot find class with name:", name)
            exit()

    # Used in debug
    def explainBlock(self):
        s = "---Explain Block---\nNode type: " + str(self.currentNode.type) + "\nReason for block: "
        if self.blockedByReturn:
            s += "Blocked by return"
        elif self.currentNode.isBlocked():
            s += "Other"
        else:
            s += "Invalid reason (something broke, or is not actualy blocked)"
        s += "\n-------------------"
        print(s)

    def isCurrentlyBlocked(self):
        return self.blockedByReturn or self.currentNode.isBlocked()

    def findCurrentFunctionCallCtx(self):
        node = self.currentNode
        while node is not None and node.type is not NodeType.FUNCTION_CALL and node.type is not NodeType.OBJECT_FUNCTION_CALL:
            node = node.parent
        if node is None:
            print("Internal error, resolving function call failed.")
            exit()
        else:
            return node.ctx

    def addFunctionNode(self, ctx:privetonParser.Fun_defContext):
        self.currentNode.addFunctionNode(ctx)

    def searchFunctionNode(self, funcName):
        node = self.currentNode
        while node is not None:
            if funcName in node.functionNodes:
                return node.functionNodes[funcName]
            node = node.parent
        # print("Function with name "+funcName+" does not exit.")
        # exit()

    def findFunctionEvaluation(self, ctx:privetonParser.Func_callContext):
        if ctx in self.functionCallEvaluations:
            # Return evaluation if it exists (function has a 'return')
            return self.functionCallEvaluations[ctx]
        else:
            # Functions return None by default
            return None

    def enterAndAddChildToCurrentNode(self, ctx, type):
        self.currentNode.children.append(ContextTreeNode(ctx, self.currentNode, type))
        self.currentNode = self.currentNode.children[-1]

    def reenterChildNode(self, node):
        if node not in self.currentNode.children:
            self.currentNode.children.append(node)
            node.parent = self.currentNode
        self.currentNode = node

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
        print("No variable "+str(name)+" found in outer scope.")
        exit()
        # self.currentNode.addVariable(name, value)

    def addVariable(self, name, value):
        self.currentNode.variable_names_map[name] = value

    def addExpression(self, ctx, value):
        self.currentNode.addExpression(ctx, value)

    def searchVariableInFunctionContext(self, node, variableName):
        # Checks if current node is function call context, if so searches for the variable in it
        if node.type == NodeType.FUNCTION_CALL or node.type == NodeType.OBJECT_FUNCTION_CALL:
            # Find the function that is being ran, through name stored in the call that is being executed
            if node.type == NodeType.FUNCTION_CALL:
                funcNode = self.searchFunctionNode(node.ctx.NAME().__str__())
            else:
                funcNode = self.searchFunctionNode(node.ctx.NAME(1).__str__())
            # Check if function contains the name that is used, if so return the value.
            if funcNode is not None and variableName in funcNode.funcArgs:
                return funcNode.funcArgs[variableName]
        return None

    def searchVariable(self, variableName):
        # Try to find it in current context, if it's a function context
        maybeVariable = self.searchVariableInFunctionContext(self.currentNode, variableName)
        if maybeVariable is not None:
            return maybeVariable

        # Search in local context
        if variableName in self.currentNode.variable_names_map:
            return self.currentNode.variable_names_map[variableName]

        # Search in external context
        return self.searchOuterVariable(variableName)

    def searchOuterVariable(self, variableName):
        tempNode = self.currentNode.parent
        while tempNode is not None:

            # Check in normal variables
            if variableName in tempNode.variable_names_map:
                return tempNode.variable_names_map[variableName]

            maybeVariable = self.searchVariableInFunctionContext(tempNode, variableName)
            if maybeVariable is not None:
                return maybeVariable

            tempNode = tempNode.parent
        print("VARIABLE WITH NAME " + str(variableName) + " NOT FOUND IN OUTER SCOPE")
        exit()

    def searchExpression(self, expression):
        tempNode = self.currentNode
        while tempNode is not None:
            if expression in tempNode.expressions_value_map:
                return tempNode.expressions_value_map[expression]
            tempNode = tempNode.parent
        print("EXPRESSION: " + str(expression.getText()) + " NOT FOUND")
        exit()

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
        self.private_variable_names_map = {}
        self.objectNodesMap = {}

        self.functionNodes = {}

        self.conditionNode = None

        self.blocked = False

        self.funcArgs = {}

    def addFunctionNode(self, ctx:privetonParser.Fun_defContext):
        funcName = ctx.NAME().__str__()
        # Saving function in a local map
        self.functionNodes[funcName] = ContextTreeNode(ctx, None, NodeType.FUNCTION)
        # Saving function argument names with None values
        for varArg in ctx.var():
            self.functionNodes[funcName].funcArgs[varArg.getText()] = None

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
