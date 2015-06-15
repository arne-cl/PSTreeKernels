
from pkg_resources import resource_filename

from preprocess import RawData
from PST import AAKNode, PSTree
from train import train_question_classification
from tree import Tree, TreeNode, Utilities


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
    pst, M = train_question_classification(fine_grained_labels=True, normalized_pst=True)

    #Extract labels from sentences of the test set:
    raw_test_file = resource_filename('PSTreeKernels', 'data/question_classification_test.txt')
    rawData_test = RawData(raw_test_file, 'question_classification_test_sents.txt', fine_grained=True)

    #Get linear trees from stanford parser test file:
    parsed_test_file = resource_filename('PSTreeKernels', 'data/question_classification_test_sents_parsed.txt')
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
