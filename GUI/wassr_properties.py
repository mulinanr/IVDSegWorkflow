
algorithmList = ['L', 'O', 'B', 'BSpline', 'BSplineG', 'M', 'MS', 'I']

class WassrProperties(object):

    def __init__(self, sSlide = '1', hStep = '0.01', maxOffset = '1.0', alternating = 'False', nDynamics = '22', lmo = 'B', gauss = '3.0', zFilter = 'False'):
        self.sSlide = sSlide
        self.hStep = hStep
        self.maxOffset = maxOffset
        self.alternating = alternating
        self.nDynamics = nDynamics
        self.lmo = lmo
        self.gauss = gauss
        self.zFilter = zFilter


