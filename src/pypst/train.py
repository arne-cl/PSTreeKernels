
from pkg_resources import resource_filename

from preprocess import RawData
from PST import PSTree
from tree import Tree, Utilities


def train_question_classification(fine_grained_labels=True, normalized_pst=True):
    #Extract labels from sentences of the training set:
    raw_training_file = resource_filename('pypst', 'data/question_classification_train.txt')
    rawData_train = RawData(raw_training_file, 'question_classification_train_sents.txt', fine_grained=fine_grained_labels)

    #Get linear trees from stanford parser training file:
    parsed_training_file = resource_filename('pypst', 'data/question_classification_train_sents_parsed.txt')
    linearTrees_train = Utilities.getLinearTrees(parsed_training_file)

    #Add all training ST's to PST:
    pst = PSTree(normalize=normalized_pst)
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
    return pst, M
