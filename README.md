Code for handling VAMAS files output by CasaXPS.

Based on the VAMAS file specification

    'VAMAS Surface Chemical Analysis Standard Data Transfer Format with Skeleton Decoding Programs'
       W.A. Dench, L.B. Hazell, M.P. Seah, and the VAMAS Community
       Surface and Interface Analysis, Volume 13, pages 63-122 (1988)

https://analyticalsciencejournals.onlinelibrary.wiley.com/doi/epdf/10.1002/sia.740130202

All VAMAS files can be parsed into the provided VAMASparser class and then accessed via the provided
get functions, so long as the user knows the names of the desired VAMAS variables. However, this
is primarily focused on reading XPS data output by the Phi Versaprobe II.

To read and plot VAMAS files for XPS spectra or depth profiles, set up a config file like the examples, 
change the config_file name in main.py, and run.

In general, parsing other VAMAS files and read out data for other kinds of plots should look something like
this:

`parser = VAMASparser('filename')`

`x, label, units = parser.get_x_vals(block_index)`

`y, label, units = parser.get_y_vals(variable_index, block_index)`

`plot_title = parser.get_block_data(VAMASBlockHeader.block_identifier, block_index)`

## VAMASspecs.py

Provides Enums for different VAMAS data types

## VAMASparse.py

Defines the VAMASparser class based on the VAMAS file specification

## vamas_helpers.py

Helper functions for dealing with Phi Versaprobe II data
