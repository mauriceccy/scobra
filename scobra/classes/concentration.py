#import pandas
from .matrix import matrix

class concentration(dict):

    def __init__(self, *args, **kwargs):
        # if type(self) == pandas.core.series.Series:
        #     fd = {}
        #     for r in self.axes[0]:
        #         fd[r] = self[r]
        super(concentration, self).__init__(*args, **kwargs)

    def __call__(self, string=''):
        mv = concentration()


    
