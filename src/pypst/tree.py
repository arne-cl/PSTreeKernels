
class TreeNode:
    '''
    Class responsible for holding a generic Tree node

    Attributes
    ----------
    value : str
        the ID of the node, e.g. a syntactical category like 'NP' or 'VB'
    parent : TreeNode or None
        a tree node that represents the parent of this one. If this node
        is the root node, its parent attribute is None.
        TODO: it is initialised as ''. does it ever keep that value?
    children: list of TreeNode
        a list of ``TreeNode``s which represent the children of this node
    '''
    def __init__(self):
        self.value = ''
        self.parent = ''
        self.children = []
    
    def setValue(self, v):
        '''set the ID (str) of this node, e.g. "NP"'''
        self.value = v
    
    def setParent(self, tn):
        '''set the parent node (TreeNode) of this node'''
        self.parent = tn
        
    def addChild(self, c):
        '''add a child (TreeNode) to the list of children of this node'''
        self.children.append(c)


class Tree:
    '''
    Class responsible for holding a generic Tree

    Attributes
    ----------
    root : TreeNode or None
        holds the root node of the tree or None, if the tree doesn't have
        any nodes
    '''
    def __init__(self, treeString=None):
        '''
        Parameters
        ----------
        treeString : str or None
            If present, the tree will be created from a parse tree string.
            Otherwise, an empty tree will be created.
        '''
        if treeString == None:
            self.root = None
        else:
            self.root = self.createTreeFromString(treeString)
            self.root.setParent(None)
        
    def printTree(self):
        '''print the complete tree'''
        self.printNode(self.root, 0)
        
    def printNode(self, node, tabulation):
        '''
        prints a subtree, i.e. a tree node and all its descendants

        Parameters
        ----------
        node : TreeNode
            the root node of the subtree to be printed
        tabulation : int
            indent the subtree with n tabs
        '''
        prefix = ''
        for i in range(0, tabulation):
            prefix = prefix + '\t'
        print(prefix+node.value)
        for child in node.children:
            self.printNode(child, tabulation+1)

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
