
from pkg_resources import resource_filename
from tree import Tree, TreeNode, AAKNode, Utilities


class EFTK:
    
    def __init__(self, node, pst):
        self.matches = set([])
        if node.value in pst.root.posVector[0].keys():
            self.matches.update(pst.root.posVector[0][node.value].ruleList)
            if len(node.children[0].children)>0:
                self.matchChildren(node.children, pst.root.posVector[0][node.value])

    def matchChildren(self, children, pstnode):
        if len(self.matches)>0:
            if len(children)>len(pstnode.posVector):
                self.matches = set([])
            else:
                for i in range(0, len(children)):
                    child = children[i]
                    if child.value in pstnode.posVector[i].keys():
                        self.matches = self.matches & pstnode.posVector[i][child.value].ruleList
                        if len(child.children[0].children)>0 and len(self.matches)>0:
                            self.matchChildren(child.children, pstnode.posVector[i][child.value])
                    else:
                        self.matches = set([])

class RawData:
    
    def __init__(self, inPath, outPath):
        self.labels = []

        inTrain = open(inPath, 'r')
        outTrain = open(outPath, 'w')
        for line in inTrain:
            data = line.split()
            self.labels.append(data[0].strip()[0:data[0].strip().find(':')])
            sentence = ''
            for i in range(1, len(data)):
                sentence += data[i] + ' '
            sentence = sentence.strip()
            outTrain.write(sentence + '\n')
            
        inTrain.close()
        outTrain.close()


class PSTree:
    def __init__(self):
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
            self.addNodeToPST(tree.root, id, self.root.posVector[0], self.root)
        elif isinstance(tree, TreeNode):
            self.prevAmount = self.currAmount
            self.addNodeToPST(tree, id, self.root.posVector[0], self.root)
        
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
    rawData_train = RawData(raw_training_file, 'question_classification_train_sents.txt')

    #Get linear trees from stanford parser training file:
    parsed_training_file = resource_filename('pypst', 'data/question_classification_train_sents_parsed.txt')
    linearTrees_train = Utilities.getLinearTrees(parsed_training_file)


    #Add all training ST's to PST:
    nodecount = []
    nodemeans = []
    nodemean = 0

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
    rawData_test = RawData(raw_test_file, 'question_classification_test_sents.txt')

    #Get linear trees from stanford parser test file:
    parsed_test_file = resource_filename('pypst', 'data/question_classification_test_sents_parsed.txt')
    linearTrees = Utilities.getLinearTrees(parsed_test_file)

    #Classify test sentences:
    for string in linearTrees:
        K = {}
        tree = Tree(string)
        
        pile = [tree.root]
        while len(pile)>0:
            node = pile[0]
            pile.remove(node)
            if len(node.children[0].children)>0:
                pile.extend(node.children)
               
            matches = EFTK(node, pst).matches
            for match in matches:
                eqID = M[match]
                if eqID in K.keys():
                    K[eqID] += 1
                else:
                    K[eqID] = 1


if __name__ == '__main__':
    main()
