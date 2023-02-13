import matplotlib.pyplot as plt 
import matplotlib as mpl
import numpy as np
from scipy.signal import find_peaks

from VAMASparse import VAMASparser

# selected XPS binding energies (from ThermoFisher)
xps_energies = {
    'Sn':485.2, 'SnO':486, 'SnO2':486.6,
    'In':443.8, 'In2O3':444, 'In2O3 3p3/2': 666.4,
    'O (metal)': 529, 'C-O':533, 'C=O':532,
    'Na': 1071,
    'C-C': 284.8, 'C-O-C': 286, 'O-C=O': 288.5
}

def plot_spectra(parsers, labels, colors, offset=0, prominence=650, id=False):
    for i, (parser, label, color) in enumerate(zip(parsers, labels, colors)):
        x, y, xunits, xlabel, yunits, ylabel  = get_binding_vs_y(parser)

        x = np.array(x)
        y = np.array(y)
        plt.plot(x, y+i*offset, label=label, color=color)
        # prominence = 650 was basically the magic number for ITO spectra; may need to adjust for others
        peaks, properties = find_peaks(y, prominence=prominence)

        if id:
            plt.plot(x[peaks], (y+i*offset)[peaks], 'x')
            print(x[peaks])
            for label, energy in xps_energies.items():
                plt.axvline(x=energy)
                plt.text(energy+0.1, 0, label)

    plot_formatting(x, xunits, yunits, ylabel)
    plt.show()
    return x, y

def get_binding_vs_y(parser, block_index=0):
    x, xlabel, xunits = parser.get_x_vals(block_index)
    x_binding = [parser.kinetic_to_binding_energy(xi) for xi in x]
    y, ylabel, yunits = parser.get_y_vals(0, block_index)

    return x_binding, y, xunits, xlabel, yunits, ylabel

def plot_formatting(x, xunits, yunits, ylabel, legend=True):
    plt.xlim(max(x)+1, min(x)-1)
    plt.xlabel('Binding Energy ['+xunits+']')
    plt.ylabel(ylabel +' [a.u.]')

    plt.tick_params(
        axis='y',          # changes apply to the x-axis
        which='both',      # both major and minor ticks are affected
        left=False,      # ticks along the bottom edge are off
        labelleft=False
        )

    if legend:
        plt.legend()

def colorFader(c1, c2, mix=0):
    '''
    credit to Markus Dutschke on Stack Overflow for this one
    '''
    c1 = np.array(mpl.colors.to_rgb(c1))
    c2 = np.array(mpl.colors.to_rgb(c2))
    return mpl.colors.to_hex((1-mix)*c1 + mix*c2)

def read_acsummry(filename):
    '''
    read the data out of an acsummry.txt file from the XPS
    '''
    is_data = False
    counter = 0

    x = []

    with open(filename) as f:
        read_data = f.read().splitlines()
        for line in read_data:
            words = line.split()
            # skip header details
            if not is_data and len(words) == 0:
                pass
            elif not is_data and not words[0] == 'Abscissa':
                pass 
            # get column labels
            elif not is_data and words[0] == 'Abscissa':
                is_data = True
                labels = words[1:]
                ys = [[] for i in range(len(labels))]
            # skip RSF/CorrectedRSF lines
            elif is_data and counter < 2:
                counter += 1
            # break to skip Mean/Standard Deviation lines
            elif is_data and len(words) == 0:
                break
            # append percent concentration data
            elif is_data: 
                x.append(float(words[0]))
                for i, word in enumerate(words[1:]):
                    ys[i].append(float(word))
    return x, ys, labels