import matplotlib.pyplot as plt 
import numpy as np

from VAMASparse import VAMASparser

def plot_spectra(filepath, filenames, labels, colors, offset=0):
    for i, (filename, label, color) in enumerate(zip(filenames, labels, colors)):
        parser = VAMASparser(filepath+filename)

        experiment, blocks = parser.read_VAMAS()

        x, y, xunits, xlabel, yunits, ylabel  = get_binding_vs_y(parser)

        x = np.array(x)
        y = np.array(y)
        plt.plot(x, y+i*offset, label=label, color=color)
    plot_formatting(x, xunits, yunits, ylabel)
    plt.show()

def get_binding_vs_y(parser):
    x, xlabel, xunits = parser.get_x_vals()
    x_binding = [parser.kinetic_to_binding_energy(xi) for xi in x]
    y, ylabel, yunits = parser.get_y_vals(0)

    return x_binding, y, xunits, xlabel, yunits, ylabel

def plot_formatting(x, xunits, yunits, ylabel):
    plt.xlim(max(x)+1, min(x)-1)
    plt.xlabel('Binding Energy ['+xunits+']')
    plt.ylabel(ylabel +' ['+yunits+']')

    plt.legend()