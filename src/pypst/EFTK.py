
from pkg_resources import resource_filename

from preprocess import RawData
from PST import AAKNode, PSTree
from train import train_question_classification
from tree import Tree, TreeNode, Utilities


class EFTK:
    '''
    Attributes
    ----------
    matches : set of int
        set of sentences (sentence indices), which contain a matching
        (sub)tree
    '''
    def __init__(self, node, pst):
        '''
        Parameters
        ----------
        node : TreeNode
            a tree node representing a (sub)tree
        pst : PSTree
            a positional suffix tree representing a number of (sub)trees
            that the TreeNode will be compared against
        '''
        self.matches = set([])
        # TODO: add all sentences (i.e. their int index) to ``self.matches``,
        #       which have the given node label in the first position
        #       (in their constituency parse tree)
        if node.value in pst.root.posVector[0].keys():
            self.matches.update(pst.root.posVector[0][node.value].ruleList)
            # TODO: if the node has any non-leaf/non-token children,
            #       match them against the PST node / AAKNode of the node
            #       label in the first position
            if len(node.children[0].children)>0:
                self.matchChildren(node.children, pst.root.posVector[0][node.value])

    def matchChildren(self, children, pstnode):
        '''
        Parameters
        ----------
        children : list of TreeNode
            a list of tree nodes, which are children of the same tree node
            parent
        pstnode : AAKNode
            the positional suffix tree node against which the child tree nodes
            are compared against
        '''
        if len(self.matches)>0:
            # there can't be any matches, if there are more child nodes
            # than positions in the AAKNode
            if len(children)>len(pstnode.posVector):
                self.matches = set([])
            else:  # finding matches is at least plausible
                # iterate over all child nodes (with recursion over all
                # grandchildren).
                # find child node labels which occured in the same tree
                # position in the training data.
                # ``self.matches`` now becomes the intersection of those
                # sentences which matched the parent node AND the child
                # node(s)
                for i in range(0, len(children)):
                    child = children[i]
                    if child.value in pstnode.posVector[i].keys():
                        self.matches = self.matches & pstnode.posVector[i][child.value].ruleList
                        if len(child.children[0].children)>0 and len(self.matches)>0:
                            self.matchChildren(child.children, pstnode.posVector[i][child.value])
                    else:
                        self.matches = set([])


def main():
    pst, M = train_question_classification(fine_grained_labels=False, normalized_pst=False)

    #Extract labels from sentences of the test set:
    raw_test_file = resource_filename('pypst', 'data/question_classification_test.txt')
    rawData_test = RawData(raw_test_file, 'question_classification_test_sents.txt', fine_grained=False)

    #Get linear trees from stanford parser test file:
    parsed_test_file = resource_filename('pypst', 'data/question_classification_test_sents_parsed.txt')
    linearTrees_test = Utilities.getLinearTrees(parsed_test_file)

    #Classify test sentences:
    for string in linearTrees_test:
        # maps from a subtree (int) to its frequency (int) in the training datas
        K = {}
        tree = Tree(string)

        # pile will hold a list of Tree node instances
        pile = [tree.root]

        # iterate over the root TreeNode of the tree and all its
        # non-leaf/non-token descendants
        while len(pile)>0:
            node = pile[0]
            pile.remove(node)
            if len(node.children[0].children)>0:
                pile.extend(node.children)

            # look up how often the given TreeNode (i.e. a (sub)tree occurs
            # in the training data (represented by the PSTree)
            matches = EFTK(node, pst).matches
            for match in matches:
                eqID = M[match]
                if eqID in K.keys():
                    K[eqID] += 1
                else:
                    K[eqID] = 1


if __name__ == '__main__':
    main()
