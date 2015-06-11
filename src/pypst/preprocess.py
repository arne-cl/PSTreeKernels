

class RawData:
    
    def __init__(self, inPath, outPath, fine_grained=True):
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
