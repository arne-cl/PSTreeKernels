
from pkg_resources import resource_filename

from preprocess import RawData
from PST import PSTree
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


def main():
    #Extract labels from sentences of the training set:
    raw_training_file = resource_filename('pypst', 'data/question_classification_train.txt')
    rawData_train = RawData(raw_training_file, 'question_classification_train_sents.txt', fine_grained=False)

    #Get linear trees from stanford parser training file:
    parsed_training_file = resource_filename('pypst', 'data/question_classification_train_sents_parsed.txt')
    linearTrees_train = Utilities.getLinearTrees(parsed_training_file)

    #Add all training ST's to PST:
    pst = PSTree(normalize=False)
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
    rawData_test = RawData(raw_test_file, 'question_classification_test_sents.txt', fine_grained=False)

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
