from algorithm import Algorithm

class MscfAlgorithm(Algorithm):

    def __init__(self, hStep, maxOffset, maxShift):
        self.hStep = hStep
        self.maxOffset = maxOffset
        self.maxShift = maxShift

    def calculate(self, mppmValue, minimalValue):
        #print('MscfAlgorithm')
        return (None, None, None, None)
