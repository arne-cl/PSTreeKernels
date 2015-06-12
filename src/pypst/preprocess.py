

class RawData:
    '''
    Converts files from a question classification dataset and stores their
    labels in the ``self.labels`` attribute (list of str).

    The input files contain lines like these:
    
        NUM:dist How far is it from Denver to Aspen ?
        LOC:city What county is Modesto , California in ?

    Here, each line consists of a label (e.g. 'NUM:dist') and a sentence.
    In the output files, only the sentences will remain.

    Attributes
    ----------
    labels : list of str
        a list of labels from the question classification input file
    '''
    def __init__(self, inPath, outPath, fine_grained=True):
        '''
        Parameters
        ----------
        inPath : str
            path to the question classification input file
        outPath: str
            path to the question classification output file, which will
            only contain the sentences (without their labels)
        fine_grained : bool
            If True, complete labels will be stored the labels attribute
            (e.g. 'LOC:city'). Otherwise, only the first part of the label
            (e.g. 'LOC') will be stored.
        '''
        self.labels = []

        inTrain = open(inPath, 'r')
        outTrain = open(outPath, 'w')
        for line in inTrain:
            data = line.split()
            if fine_grained:
                self.labels.append(data[0].strip())
            else:
                self.labels.append(data[0].strip()[0:data[0].strip().find(':')])
            sentence = ''
            for i in range(1, len(data)):
                sentence += data[i] + ' '
            sentence = sentence.strip()
            outTrain.write(sentence + '\n')

        inTrain.close()
        outTrain.close()
