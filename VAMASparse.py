'''
Based on the VAMAS file specification
    VAMAS Surface Chemical Analysis Standard Data Transfer Format with Skeleton Decoding Programs'
       W.A. Dench, L.B. Hazell, M.P. Seah, and the VAMAS Community
       Surface and Interface Analysis, Volume 13, pages 63-122 (1988)
as implemented in https://github.com/aeronth/wraith.git for Python 2

# A note on units standardized in the VAMAS 1988 specification:
# units = ( 'c/s' | 'd' | 'degree' | 'eV' | 'K' | 'micro C' | 'micro m' | 'm/s' | 'n' | 'nA' | 'ps' | 's' | 'u' | 'V')
# These values are abbreviations for the units listed below:
#  'c/s'      counts per second
#  'd'        dimensionless - just a number, e.g. counts per channel
#  'degree'   angle in degrees
#  'eV'       eletron volts
#  'K'        Kelvin
#  'micro C'  microcoulombs
#  'micro m'  micrometres
#  'm/s'      metres per second
#  'n'        not defined here - may be given in a lobel
#  'nA'       nanoamps
#  'ps'       picoseconds
#  's'        seconds
#  'u'        unified atomic mass units
#  'V'        volts
'''

from datetime import datetime 
import scipy 
from numpy import arange, array 

class VAMASExperiment:
    def __init__(self, filename):
        self.filename = filename
        self.exp_metadata_labels = (
            'format_identifier',
            'institution_identifier',
            'instrument_model_identifier',
            'operator_identifier',
            'experiment_identifier',
            'number_of_lines_in_comment'
        )
        self.structure_metadata_labels = (
            'experiment_mode',
            'scan_mode',
        )

    def read_from_file(self):
        '''
        BASIC VAMAS FILESTRUCTURE:
            - experiment metadata
            - comment
            - file structure metadata
        
        '''
        with open(self.filename) as file:
            self.exp_metadata = dict(self.exp_metadata_labels)
            

            exp_metadata_filled = False 
            comment_filled = False 
            structure_metadata_filled = False
            for i, line in enumerate(file):
                if not exp_metadata_filled:
                    pass 
                elif not comment_filled:
                    pass 
                elif not structure_metadata_filled:
                    pass