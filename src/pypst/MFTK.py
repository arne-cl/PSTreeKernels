
from pkg_resources import resource_filename

from preprocess import RawData
from PST import PSTree
from tree import Tree, TreeNode, AAKNode, Utilities


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


def main():
    #Extract labels from sentences of the training set:
    raw_training_file = resource_filename('pypst', 'data/question_classification_train.txt')
    rawData_train = RawData(raw_training_file, 'question_classification_train_sents.txt', fine_grained=True)

    #Get linear trees from stanford parser training file:
    parsed_training_file = resource_filename('pypst', 'data/question_classification_train_sents_parsed.txt')
    linearTrees_train = Utilities.getLinearTrees(parsed_training_file)

    #Add all training ST's to PST:
    pst = PSTree(normalize=True)
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
