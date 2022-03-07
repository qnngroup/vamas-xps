Code for handling VAMAS files output by CasaXPS.

Based on the VAMAS file specification

    'VAMAS Surface Chemical Analysis Standard Data Transfer Format with Skeleton Decoding Programs'
       W.A. Dench, L.B. Hazell, M.P. Seah, and the VAMAS Community
       Surface and Interface Analysis, Volume 13, pages 63-122 (1988)

https://analyticalsciencejournals.onlinelibrary.wiley.com/doi/epdf/10.1002/sia.740130202

Example usage in vamas_scripts.py. Basically, the VAMASparser class reads the VAMAS file into
1) a dictionary containing Experiment section data and 2) a list of dictionaries containing Blocks
data. There are some simple getter functions for retrieving x-axis (abscissa) and y-axis (ordinate)
values; other data can be retrieved through Enum values seen in VAMASspecs.py