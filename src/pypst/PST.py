
from tree import Tree, TreeNode


class PSTree:
    '''
    Class responsible for holding a Positional Suffix Tree

    Attributes
    ----------
    normalized : bool
        TODO
    normValues : dict
        TODO: maps from an int (called 'id' in addTreeToPST) to its normalization
        value (int)
        NOTE: this attribute is only present iff self.normalized is True!

    root : AAKNode
        TODO
    prevAmount : int
        TODO
    currAmount : int
        TODO seems to count the number of unique node IDs
    totalAmount : int
        total amount of nodes added to the tree
    savedAmount : int
        TODO seems to count the number of nodes whose ID occurs more than
             once
    '''
    def __init__(self, normalize=True):
        self.normalized = normalize
        if self.normalized:
            self.normValues = {}

        self.root = AAKNode()
        self.root.setValue('None')
        self.root.setParent('None')
        self.root.posVector.append({})

        self.prevAmount = 0;
        self.currAmount = 0;
        self.totalAmount = 0;
        self.savedAmount = 0;

    def addTreeToPST(self, tree, id):
        '''
        Adds a Tree or TreeNode to the PST. If it is a normalized PST,
        a normalization value is stored in ``self.normValues`` under the
        given node index.

        Parameters
        ----------
        tree : Tree or TreeNode
            TODO
        id : int
            TODO: the 'current index' of the tree node to be added
        '''
        if isinstance(tree, Tree):
            self.prevAmount = self.currAmount
            if self.normalized:
                self.normValues[id] = self.getNormalizationValue(tree.root)
            self.addNodeToPST(tree.root, id, self.root.posVector[0], self.root)
        elif isinstance(tree, TreeNode):
            self.prevAmount = self.currAmount
            if self.normalized and tree.parent==None:
                self.normValues[id] = self.getNormalization(tree)
            self.addNodeToPST(tree, id, self.root.posVector[0], self.root)

    def getNormalization(self, root):
        result = 0
        pile = [root]
        while len(pile)>0:
            aux = pile[0]
            pile.remove(aux)
            pile.extend(aux.children)
            result += self.getNormalizationValue(aux)
        return result

    def getNormalizationValue(self, node):
        if len(node.children)==0:
            return 1
        else:
            result = 1
            for child in node.children:
                result *= 1+self.getNormalizationValue(child)
            return result

    def addNodeToPST(self, node, id, dict, parent):
        '''
        adds a TreeNode to the PST

        Parameters
        ----------
        node : TreeNode
            TODO
        id : int
            TODO
        dict : dict
            maps a node ID / category (str) to an AAKNode
            TODO explain the posVector position (nth child)
        parent : AAKNode
            the parent node of the AAKNode corresponding to the given TreeNode
        '''
        self.totalAmount += 1
        # we have already processed a node with the same ID / category
        if node.value in dict.keys():
            self.savedAmount += 1
            # the AAKNode with the same ID / category as the given TreeNode
            PSTNode = dict[node.value]
            # adds the current node index as a 'rule' to the PST node / AAKNode
            PSTNode.addRule(id)

            # calls this method recursively for all children of this TreeNode.
            # if necessary, creates a new posVector element for each of the
            # children
            if len(node.children)>0:
                for i in range(0, len(node.children)):
                    if len(PSTNode.posVector)==i:
                        PSTNode.posVector.append({})
                    self.addNodeToPST(node.children[i], id, PSTNode.posVector[i], PSTNode)

        # this is the first time we process a node with this ID / category
        else:
            self.currAmount += 1
            # create a new PST node / AAKNode and initialise it
            # with ID and current index as rule
            # TODO add value/parent to AAKNode init?
            PSTNode = AAKNode()
            PSTNode.setValue(node.value)
            PSTNode.setParent(parent)
            PSTNode.addRule(id)
            # store PST node in dict
            dict[node.value] = PSTNode

            # TODO get rid of duplicated code
            # calls this method recursively for all children of this TreeNode.
            # if necessary, creates a new posVector element for each of the
            # children
            if len(node.children)>0:
                for i in range(0, len(node.children)):
                    if len(PSTNode.posVector)==i:
                        PSTNode.posVector.append({})
                    self.addNodeToPST(node.children[i], id, PSTNode.posVector[i], PSTNode)

    def printPSTree(self):
        self.printPSTNode(self.root, 0)

    def printPSTNode(self, node, tabulation):
        prefix = ''
        for i in range(0, tabulation):
            prefix = prefix + '\t'

        print(prefix + 'Value: ' + node.value)
        print(prefix + 'Rules:')
        for rule in node.ruleList:
            print(prefix + '\t' + rule)
        print(prefix + 'Vector Positions:')
        for i in range(0, len(node.posVector)):
            print(prefix + '\t Position ' + str(i) + ':')
            for key in node.posVector[i]:
                self.printPSTNode(node.posVector[i][key], tabulation+1)


class AAKNode:
    '''
    Holds the information of an Agile Adaptive Knowledge Tree's node.

    Attributes
    ----------
    value : str
        the ID of the node, e.g. a syntacticategory like 'NP' or 'None'
        TODO: why is None used as a str and not a bool?
    parent : AAKNode or str
        the AAKNode that is the parent of this one or 'None', if this
        node is root node
        TODO: why is None used as a str and not a bool?
        TODO: what kind of root node is an AAKNode without a parent?

            >>> an = pst.root
            >>> dtan = an.posVector[0]['DT']
            >>> dtan.parent
            <PST.AAKNode instance at 0x7fa3a531ebd8>
            >>> dtan.parent.value
            'None'

    ruleList : set of int
        TODO: what is this set of integers used for?
    posVector: list of dict
        TODO: the list contains dictionaries (one for each position in
              the tree). each dict maps a node label (str) to an AAKNode
    alignments : dict
        TODO
    '''
    def __init__(self):
        self.value = ''
        self.parent = ''
        self.ruleList = set([])
        self.posVector = []
        self.alignments = {}

    def setParent(self, p):
        '''set parent node (AAKNode) of this node'''
        self.parent = p

    def setValue(self, v):
        '''set ID (str, e.g. 'NP') of this node or "None"'''
        self.value = v

    def addRule(self, r):
        '''
        add rule (int) to this node
        TODO: what are the rules used for?
        '''
        self.ruleList.add(r)
