import matplotlib.pyplot as plt

from VAMASparse import VAMASparser
from VAMASspecs import VAMASExperimentOptions

filepath = '/home/emmabat/Documents/XPS/211216/'
filename = '103.1.itosa5ei_depth.vms'

parser = VAMASparser(filepath+filename)

experiment, blocks = parser.read_VAMAS()

'''
y = parser.get_ordinate_vals(0)
plt.plot(y)
plt.show()
'''