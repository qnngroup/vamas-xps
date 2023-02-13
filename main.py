import matplotlib.pyplot as plt
import matplotlib.colors
import matplotlib as mpl
import numpy as np
import json
from enum import Enum, auto
import tikzplotlib

from VAMASparse import VAMASparser
from VAMASspecs import *
from vamas_helpers import *

class PlotType(Enum):
    spectra = auto()
    high_res = auto()
    depth = auto()

def main():
    config_folder = 'configs/'
    config_file = 'ITOSAcontrol_depth.json'
    # this variable inserts a vertical offset between spectra for readability
    # recommended to adjust until it looks right
    offset = 5000

    id_to_peak = {'In':'Indium 3d5', 'Sn': 'Tin 3d', 'O': 'Oxygen 1s', 'C': 'Carbon 1s'}

    SMALL_SIZE = 12
    MEDIUM_SIZE = 14
    BIGGER_SIZE = 16

    plt.rc('font', size=SMALL_SIZE)          # controls default text sizes
    plt.rc('axes', titlesize=SMALL_SIZE)     # fontsize of the axes title
    plt.rc('axes', labelsize=MEDIUM_SIZE)    # fontsize of the x and y labels
    plt.rc('xtick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
    plt.rc('ytick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
    plt.rc('legend', fontsize=SMALL_SIZE)    # legend fontsize
    plt.rc('figure', titlesize=BIGGER_SIZE)  # fontsize of the figure title


    with open(config_folder+config_file) as json_file:
        config = json.load(json_file)
        filepath = config['filepath']
        filenames = config['filenames']
        labels = config['labels']
        colors = config['colors']
        plotType = PlotType[config['plot type']]

    parsers = []
    for filename in filenames:
        parser = VAMASparser(filepath+filename)
        experiment, blocks = parser.read_VAMAS()

        parsers.append(parser)

    if plotType == PlotType.spectra:
        x, y = plot_spectra(parsers, labels, colors, offset)

    elif plotType == PlotType.high_res:
        for i in range(len(blocks)):
            for j, parser in enumerate(parsers):
                x, y, xunits, xlabel, yunits, ylabel = get_binding_vs_y(parser)
                block_identifier = parser.get_block_data(VAMASBlockHeader.block_identifier, i)
                plt.plot(x, y, label=labels[j], color=colors[j])

            plot_formatting(x, xunits, yunits, ylabel)
            plt.title(block_identifier)
            plt.show()
    elif plotType == PlotType.depth:
        unique_identifiers = {}
        for parser in parsers:
            for i in range(len(blocks)):
                for j, parser in enumerate(parsers):
                    x,  y, xunits, xlabel, yunits, ylabel = get_binding_vs_y(parser, i)
                    block_identifier = parser.get_block_data(VAMASBlockHeader.block_identifier, i)

                    if block_identifier[:2] not in unique_identifiers:
                        print(block_identifier)
                        unique_identifiers[block_identifier[:2]] = [[], []]
                    unique_identifiers[block_identifier[:2]][0].append(x)
                    unique_identifiers[block_identifier[:2]][1].append(y)

            for identifier, coords in unique_identifiers.items():
                xs = coords[0]
                ys = coords[1]
                cmap_colors = [colorFader(colors[0], colors[1], i/len(xs[1:])) for i in range(len(xs))]

                for i, (x, y) in enumerate(zip(xs[1:], ys[1:])):
                    plt.plot(x, [yi-i*offset for yi in y], color=cmap_colors[i])

                cmap = matplotlib.colors.ListedColormap(cmap_colors)
                norm = mpl.colors.Normalize(0, config['sputter stop'])
                cb1 = plt.colorbar(mpl.cm.ScalarMappable(norm=norm, cmap=cmap), label='Sputter Time [min]')
                cb1.ax.invert_yaxis()
                plot_formatting(x, xunits, yunits, ylabel, legend=False)
                plt.title(id_to_peak[identifier.strip()])
                tikzplotlib.save(identifier+'_tikzplot.tex')
                plt.savefig(identifier+'.svg')
                plt.show()
                #plt.show()
    
    if config['acsummry'] == "True":
        x, ys, elmt_labels = read_acsummry(filepath+config['acname'])
        linetypes = np.flip(['-', ':', '--', '-.'])
        for i, (y, label) in enumerate(zip(np.flip(ys, 0), np.flip(elmt_labels))):
            plt.plot(x, y, label=label, linestyle=linetypes[i], color=colorFader('black', 'gray', i/2))
        plt.xlabel('Sputter Time [min]')
        plt.ylim((0, 100))
        plt.ylabel('Atomic Concentration [%]')
        plt.legend()
        plt.savefig('acsummary.svg')
        plt.show()

if __name__ == '__main__':
    main()