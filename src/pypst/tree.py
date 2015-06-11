
class TreeNode:
    '''Class responsible for holding a generic Tree node'''
    def __init__(self):
        self.value = ''
        self.parent = ''
        self.children = []
    
    def setValue(self, v):
        self.value = v
    
    def setParent(self, tn):
        self.parent = tn
        
    def addChild(self, c):
        self.children.append(c)


class Tree:
    '''Class responsible for holding a generic Tree'''
    def __init__(self, treeString=None):
        if treeString == None:
            self.root = None
        else:
            self.root = self.createTreeFromString(treeString)
            self.root.setParent(None)
        
    def printTree(self):
        self.printNode(self.root, 0)
        
    def printNode(self, node, tabulation):
        prefix = ''
        for i in range(0, tabulation):
            prefix = prefix + '\t'
        print(prefix+node.value)
        for child in node.children:
            self.printNode(child, tabulation+1)
                
    def printTreeWithAAKData(self, pstdata):
        self.printNodeWithAAKData(self.root, 0, pstdata)
        
    def printNodeWithAAKData(self, node, tabulation, pstdata):
        prefix = ''
        for i in range(0, tabulation):
            prefix = prefix + '\t'
        print(prefix+node.value)
        if node in pstdata.link:
            PSTNode = pstdata.link[node]
            for rule in PSTNode.ruleList:
                print(prefix+rule)
        for child in node.children:
            self.printNodeWithAAKData(child, tabulation+1, pstdata)
            
    def saveTreeWithAAKData(self, pstdata, file):
        self.saveNodeWithAAKData(self.root, 0, pstdata, file)
        
    def saveNodeWithAAKData(self, node, tabulation, pstdata, file):
        prefix = ''
        for i in range(0, tabulation):
            prefix = prefix + '\t'
        file.write(prefix+node.value+'\n')
        if node in pstdata.link:
            PSTNode = pstdata.link[node]
            for rule in PSTNode.ruleList:
                file.write(prefix+rule+'\n')
        for child in node.children:
            self.saveNodeWithAAKData(child, tabulation+1, pstdata, file)
        
    def createTreeFromString(self, treeString):
        auxC = 1
        value = ''
        while not treeString[auxC]==' ':
            value = value+treeString[auxC]
            auxC = auxC+1
        value = value.strip()
        
        if not treeString[auxC+1]=='(':
            auxC = auxC+1
            child = ''
            while not treeString[auxC]==')':
                child = child+treeString[auxC]
                auxC = auxC+1
            result = TreeNode()
            result.setValue(value)
            childNode = TreeNode()
            childNode.setValue(child)
            childNode.setParent(result)
            result.addChild(childNode)
            return result
        else:
            result = TreeNode()
            result.setValue(value)
            auxC = auxC+1
            start = auxC
            level = 2
            walker = auxC+1
            while not level==0:
                if treeString[walker]=='(':
                    level = level+1
                elif treeString[walker]==')':
                    level = level-1
                    if level==1:
                        substring = treeString[start:walker+1]
                        substringNode = self.createTreeFromString(substring)
                        substringNode.setParent(result)
                        result.addChild(substringNode)
                        start = walker+1
                walker = walker+1
            return result


class AAKNode:
    '''Holds the information of an Agile Adaptive Knowledge Tree's node'''
    def __init__(self):
        self.value = ''
        self.parent = ''
        self.ruleList = set([])
        self.posVector = []
        self.alignments = {}
        
    def setParent(self, p):
        self.parent = p
        
    def setValue(self, v):
        self.value = v
        
    def addRule(self, r):
        self.ruleList.add(r)


class Utilities:
    
    @staticmethod
    def getLinearTrees(inPath):
        result = []
        
        tree = ''
        f1 = open(inPath, 'r')
        for line in f1: 
            if line.strip()=='':
                tree = tree.replace(') (', ')(')
                if not tree.strip()=='':
                    tree = tree.strip()[0:len(tree)-2]
                    result.append(tree)
                tree = ''
            else:
                if not line.strip()=='(ROOT':
                    tree = tree + line.strip() + ' ' 
        
        f1.close()
        
        return result
