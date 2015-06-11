class PSTree:
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
        self.totalAmount += 1
        if node.value in dict.keys():
            self.savedAmount += 1
            PSTNode = dict[node.value]
            PSTNode.addRule(id)
            if len(node.children)>0:
                for i in range(0, len(node.children)):
                    if len(PSTNode.posVector)==i:
                        PSTNode.posVector.append({})
                    self.addNodeToPST(node.children[i], id, PSTNode.posVector[i], PSTNode)
        else:
            self.currAmount += 1
            PSTNode = AAKNode()
            PSTNode.setValue(node.value)
            PSTNode.setParent(parent)
            PSTNode.addRule(id)
            dict[node.value] = PSTNode
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
