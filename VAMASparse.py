'''
Based on the VAMAS file specification
    VAMAS Surface Chemical Analysis Standard Data Transfer Format with Skeleton Decoding Programs'
       W.A. Dench, L.B. Hazell, M.P. Seah, and the VAMAS Community
       Surface and Interface Analysis, Volume 13, pages 63-122 (1988)
as implemented in https://github.com/aeronth/wraith.git for Python 2

Specification:
https://analyticalsciencejournals-onlinelibrary-wiley-com.libproxy.mit.edu/doi/epdf/10.1002/sia.740130202

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
        # for CasaXPS files from the Phi VersaProbe,
        # all but number_of_blocks = 1 should be 0
        self.datatype_metadata_labels = (
            'number_of_spectral_regions',
            'number_of_experimental_variables',
            'number_of_entries_in_param_list',
            'number_of_manually_entered_items',
            'number_of_future_upgrade_exp_entries',
            'number_of_future_upgrade_block_entries',
            'number_of_blocks'
        )

    def read_from_file(self):
        '''
        BASIC VAMAS FILESTRUCTURE:
            - experiment metadata
            - comment
            - file structure metadata
            - datatype metadata
            - data block 1
            - ....
            - data block N
        '''
        with open(self.filename) as file:
            self.exp_metadata = dict(self.exp_metadata_labels)
            self.comment = ""
            self.structure_metadata = dict(self.exp_metadata_labels) 
            self.datatype_metadata = dict(self.datatype_metadata_labels)  
            self.blocks = []         

            exp_metadata_filled = False 
            comment_filled = False 
            structure_metadata_filled = False
            datatype_metadata_filled = False
            block_filled = []

            index = 0
            for line in file:
                if not exp_metadata_filled:
                    # populate experiment metadata
                    self.exp_metadata[self.exp_metadata_labels[index]] = line.strip()
                    index = index + 1
                    if index >= len(self.exp_metadata_labels):
                        exp_metadata_filled = True
                        index = 0
                elif not comment_filled:
                    # populate comment based on number of lines specified in metadata
                    self.comment += line
                    index = index + 1
                    if index >= int(self.exp_metadata['number_of_lines_in_comment']):
                        comment_filled = True 
                        index = 0
                elif not structure_metadata_filled:
                    # populate structure metadata
                    self.structure_metadata[self.structure_metadata_labels[index]] = line.strip()
                    index = index + 1
                    if index >= len(self.structure_metadata_labels):
                        structure_metadata_filled = True
                        index = 0
                elif not datatype_metadata_filled:
                    # populate datatype metadata (assumes all but blocks are 0)
                    if self.structure_metadata['experiment_mode'].upper() == 'NORM':
                        self.datatype_metadata[self.datatype_metadata_labels[index]] = line
                        index = index + 1
                        if index >= len(self.datatype_metadata_labels):
                            datatype_metadata_filled = True 
                            index = 0
                            for i in range(int(self.datatype_metadata['number_of_blocks'])):
                                self.blocks.append(VAMASBlock)
                                self.block_filled.append(False)
                    else:
                        print('experiment mode not supported')
                        break
                else:
                    pass

class VAMASBlock():
    def __init__(self):
        self.metadata_labels = (
            'block_identifier',
            'sample_identifier',
            'year',
            'month',
            'day',
            'hours',
            'minutes',
            'seconds',
            'number_of_hours_in_advance_of_GMT',
            'number_of_lines_in_comment',
            'technique',
            'analysis_source_label',
            'analysis_source_characteristic_energy',
            'analysis_source_strength',
            'analysis_source_beam_width_x',
            'analysis_source_beam_width_y',
            'analysis_source_polar_AOI',
            'analysis_source_azimuth',
            'analyzer_mode',
            'analyzer_pass_energy',
            'mangification_of_anlayzer_transfer_lens',
            'analyzer_work_function',
            'target_bias',
            'analysis_width_x',
            'analysis_width_y',
            'analyzer_axis_polar_offset',
            'analyzer_axis_azimuth_offset',
            'species_label',
            'transition_state_label',
            'charge_of_detected_particle',
            'number_of_corresponding_variables',
            'signal_mode',
            'signal_collection_time',
            'number_of_scans_to_compile_block',
            'signal_time_correction',
            'sputtering_source_energy',
            'sputtering_source_beam_current',
            'sputtering_source_width_x',
            'sputtering_source_width,y',
            'sputtering_source_polar_AOI',
            'sputtering_source_azimuth',
            'sputtering_mode',
            'sample_normal_polar_tilt',
            'sample_normal_azimuth_tilt',
            'sample_rotation_angle',
            'number_of_additional_params',
            'number_of_future_upgrade_entries',
            'number_of_ordinate_values',
            'number_of_corresponding_variables'
        )