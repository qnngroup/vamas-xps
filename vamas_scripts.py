import matplotlib.pyplot as plt

from VAMASparse import VAMASparser
from VAMASspecs import VAMASExperimentOptions

filepath = '/home/emmabat/Documents/XPS/211124/'
filename = '107.6.ci.vms'

parser = VAMASparser(filepath+filename)

experiment, blocks = parser.read_VAMAS()

'''
y = parser.get_ordinate_vals(0)
plt.plot(y)
plt.show()
'''