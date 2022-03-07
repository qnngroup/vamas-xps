import matplotlib.pyplot as plt
import numpy as np
import json
from enum import Enum, auto

from VAMASparse import VAMASparser
from VAMASspecs import *
from vamas_helpers import *

class PlotType(Enum):
    spectra = auto()
    high_res = auto()

def main():
    config_folder = 'configs/'
    config_file = '211124_highres.json'

    with open(config_folder+config_file) as json_file:
        config = json.load(json_file)
        filepath = config['filepath']
        filenames = config['filenames']
        labels = config['labels']
        colors = config['colors']
        plotType = PlotType[config['plot type']]

    if plotType == PlotType.spectra:
        offset = 2000
        plot_spectra(filepath, filenames, labels, colors, offset)

    elif plotType == PlotType.high_res:
        parsers = []
        for filename, label in zip(filenames, labels):
            parser = VAMASparser(filepath+filename)

            experiment, blocks = parser.read_VAMAS()
            parsers.append(parser)

        for i in range(len(blocks)):
            for j, parser in enumerate(parsers):
                x, y, xunits, xlabel, yunits, ylabel = get_binding_vs_y(parser)
                block_identifier = parser.get_block_data(VAMASBlockHeader.block_identifier, i)
                plt.plot(x, y, label=labels[j], color=colors[j])

            plot_formatting(x, xunits, yunits, ylabel)
            plt.title(block_identifier)
            plt.show()

if __name__ == '__main__':
    main()