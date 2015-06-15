
from pkg_resources import resource_filename

from preprocess import RawData
from PST import PSTree
from tree import Tree, Utilities


def train_question_classification(fine_grained_labels=True, normalized_pst=True):
    '''
    builds a positional suffix tree from the constituency parsed question
    classification training data and a dict mapping index of a specific
    subtree (int) to the index of the sentence it was extracted from.

    Parameters
    ----------
    fine_grained_labels : bool
        If True, extracts fine grained labels from the training data
        (e.g. 'LOC:city'). Otherwise, extracts coarse grained labels,
        (e.g. 'LOC').
    normalized_pst : bool
        If True, normalises the positional suffix tree

    Returns
    -------
    pst : PSTree
        a positional suffix tree which contains all subtrees from the
        constituency parse trees from the question classification training
        set
    M : dict
        maps from the index of a specific subtree (int) to the index of the
        sentence it was extracted from
    '''
    #Extract labels from sentences of the training set:
    raw_training_file = resource_filename('PSTreeKernels', 'data/question_classification_train.txt')
    rawData_train = RawData(raw_training_file, 'question_classification_train_sents.txt', fine_grained=fine_grained_labels)

    #Get linear trees from stanford parser training file:
    parsed_training_file = resource_filename('PSTreeKernels', 'data/question_classification_train_sents_parsed.txt')
    linearTrees_train = Utilities.getLinearTrees(parsed_training_file)

    #Add all training ST's to PST:
    pst = PSTree(normalize=normalized_pst)
    M = {}
    currIndex = 0

    # convert each constituency parse into a Tree
    for i in range(0, len(linearTrees_train)):
        tree = Tree(linearTrees_train[i])
        # maps from node labels (str) to node label counts (int)
        visitedLabels = {}
        # pile will hold a list of Tree node instances
        pile = [tree.root]
        initialIndex = currIndex
        # TODO: seems to hold the count of the most used node label
        maxIndex = -1

        # iterate over the root TreeNode of the tree and all its
        # non-leaf/non-token descendants
        while len(pile)>0:
            node = pile[0]
            pile.remove(node)

            # if the node label is already known
            if node.value in visitedLabels.keys():
                shift = visitedLabels[node.value]
                # TODO: we'll need to add nodes with the same label under
                #       different indices
                pst.addTreeToPST(node, currIndex + shift)
                visitedLabels[node.value] += 1
            else:  # if the node label is new
                pst.addTreeToPST(node, currIndex)
                visitedLabels[node.value] = 1

            if visitedLabels[node.value]>maxIndex:
                maxIndex = visitedLabels[node.value]

            # add child nodes to the pile (if they aren't leaf nodes, i.e. tokens)
            if len(node.children[0].children)>0:
                pile.extend(node.children)

        for j in range(currIndex, currIndex + maxIndex):
            M[j] = i
        currIndex += maxIndex
    return pst, M
