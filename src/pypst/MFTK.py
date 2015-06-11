
from pkg_resources import resource_filename
from tree import Tree, TreeNode, AAKNode, Utilities
from preprocess import RawData


class MFTK:
    
    def __init__(self, node, pst, lambdaV, miV):
        self.scores = {}
        self.matchNode(node, pst.root.posVector[0], lambdaV, miV)
        
    def matchNode(self, node, dict, lambdaV, miV):
        if node.value in dict.keys():
            self.scores[node] = {}
            PSTNode = dict[node.value]
            IDs = PSTNode.ruleList
            if len(node.children[0].children)==0:
                for ID in IDs:
                    self.scores[node][ID] = lambdaV
            else:
                for ID in IDs:
                    self.scores[node][ID] = lambdaV
                diffSize = len(node.children)-len(PSTNode.posVector)
                for i in range(0, min(len(node.children), len(PSTNode.posVector))):
                    child = node.children[i]
                    self.matchNode(child, PSTNode.posVector[i], lambdaV, miV)
                    missedIDs = set(self.scores[node].keys()).difference(self.scores[child].keys())
                    for childID in self.scores[child].keys():
                        self.scores[node][childID] *= miV + self.scores[child][childID]
                    for childID in missedIDs:
                        self.scores[node][childID] *= miV + 0.0
                if diffSize>0:
                    for i in range(0, diffSize):
                        for ID in IDs:
                            self.scores[node][ID] *= miV
        else:
            self.scores[node] = {}


class PSTree:
    def __init__(self):
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
            self.normValues[id] = self.getNormalizationValue(tree.root)
            self.addNodeToPST(tree.root, id, self.root.posVector[0], self.root)
        elif isinstance(tree, TreeNode):
            self.prevAmount = self.currAmount
            if tree.parent==None:
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


def main():
    #Extract labels from sentences of the training set:
    raw_training_file = resource_filename('pypst', 'data/question_classification_train.txt')
    rawData_train = RawData(raw_training_file, 'question_classification_train_sents.txt', fine_grained=True)

    #Get linear trees from stanford parser training file:
    parsed_training_file = resource_filename('pypst', 'data/question_classification_train_sents_parsed.txt')
    linearTrees_train = Utilities.getLinearTrees(parsed_training_file)

    #Add all training ST's to PST:
    pst = PSTree()
    M = {}
    currIndex = 0
    for i in range(0, len(linearTrees_train)):
        tree = Tree(linearTrees_train[i])
        visitedLabels = {}
        pile = [tree.root]
        initialIndex = currIndex
        maxIndex = -1

        while len(pile)>0:
            node = pile[0]
            pile.remove(node)
            if node.value in visitedLabels.keys():
                shift = visitedLabels[node.value]
                pst.addTreeToPST(node, currIndex + shift)
                visitedLabels[node.value] += 1
            else:
                pst.addTreeToPST(node, currIndex)
                visitedLabels[node.value] = 1
            if visitedLabels[node.value]>maxIndex:
                maxIndex = visitedLabels[node.value]
            if len(node.children[0].children)>0:
                pile.extend(node.children)

        for j in range(currIndex, currIndex + maxIndex):
            M[j] = i
        currIndex += maxIndex

    #Extract labels from sentences of the test set:    
    raw_test_file = resource_filename('pypst', 'data/question_classification_test.txt')
    rawData_test = RawData(raw_test_file, 'question_classification_test_sents.txt', fine_grained=True)

    #Get linear trees from stanford parser test file:
    parsed_test_file = resource_filename('pypst', 'data/question_classification_test_sents_parsed.txt')
    linearTrees_test = Utilities.getLinearTrees(parsed_test_file)

    #Classify test sentences:
    for string in linearTrees_test:
        K = {}
        tree = Tree(string)
        
        pile = [tree.root]
        while len(pile)>0:
            node = pile[0]
            pile.remove(node)
            if len(node.children[0].children)>0:
                pile.extend(node.children)
               
            matchData = MFTK(node, pst, 1, 0)
            nodeScores = matchData.scores
            for match in nodeScores[node].keys():
                eqID = M[match]
                if eqID in K.keys():
                    K[eqID] += nodeScores[node][match]
                else:
                    K[eqID] = nodeScores[node][match]


if __name__ == '__main__':
    main()
