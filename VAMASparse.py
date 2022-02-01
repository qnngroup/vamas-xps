'''
Based on the VAMAS file specification
    VAMAS Surface Chemical Analysis Standard Data Transfer Format with Skeleton Decoding Programs'
       W.A. Dench, L.B. Hazell, M.P. Seah, and the VAMAS Community
       Surface and Interface Analysis, Volume 13, pages 63-122 (1988)
https://analyticalsciencejournals-onlinelibrary-wiley-com.libproxy.mit.edu/doi/epdf/10.1002/sia.740130202

with additional reference to https://github.com/aeronth/wraith.git for Python 2

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

from numpy import exp, expm1
from VAMASspecs import *

class VAMASparser():
    def __init__(self, filename):
        self.filename = filename 

        self.exp_numerical_labels = dict.fromkeys((
            VAMASExperimentOptions.number_of_lines_in_comment,
            VAMASExperimentOptions.number_of_spectral_regions,
            VAMASExperimentOptions.number_of_exp_variables,
            VAMASExperimentOptions.number_of_entries_include_list,
            VAMASExperimentOptions.number_of_manually_entered_items,
            VAMASExperimentOptions.number_of_future_upgrade_exp_entries,
            VAMASExperimentOptions.number_of_future_upgrade_block_entries,
            VAMASExperimentOptions.number_of_blocks
        ))

        self.exp_type_labels = dict.fromkeys((
            VAMASExperimentOptions.experiment_mode,
            VAMASExperimentOptions.scan_mode,
        ))

        self.block_numerical_labels = dict.fromkeys((
            NumberedVAMASBlockOptions.number_of_lines_in_comment,
            NumberedVAMASBlockOptions.number_of_corresponding_variables,
            NumberedVAMASBlockOptions.number_of_additional_params,
            VAMASBlockFooter.number_of_ordinate_values
        ))

        self.block_type_labels = dict.fromkeys((
            NumberedVAMASBlockOptions.technique
        ))

    def multiline_decision(self, current_lines, total_lines, index, lines_per_item=1):
        '''
        current_lines = number of lines already read
        total_lines = total number of lines to read into this variable
        index = current index into Enum

        returns: new index, current_lines, keep_multiline (Boolean), create (Boolean) 
        '''
        if current_lines >= total_lines:
            return index + lines_per_item, current_lines, False, False
        # otherwise add to comment without advancing index
        elif current_lines == 0:
            return index, current_lines + 1, True, True
        else:
            return index, current_lines + 1, True, False

    def experiment_parser(self, line, index):
        '''
        line = line of file to be read
        index = current index into Experiment spec enum

        Reads line into the appropriate key of self.VAMASExperiment (dictionary)

        returns new index & Boolean representing whether the Experiment data is all read
        '''
        option = VAMASExperimentOptions(index)
                    
        # check for optional/multiline cases
        # Multiline comment
        if option == VAMASExperimentOptions.comment:
            total_lines = self.exp_numerical_labels[VAMASExperimentOptions.number_of_lines_in_comment]
            index, self.comment_lines, multiline, create = self.multiline_decision(self.comment_lines, total_lines, index)
            if create:
                self.VAMASExperiment[option] = []
            option = VAMASExperimentOptions(index)

        # Optional: spectral regions
        if option == VAMASExperimentOptions.number_of_spectral_regions:
            if (self.exp_type_labels[VAMASExperimentOptions.experiment_mode] 
                == (ExperimentMode.MAP or ExperimentMode.MAPDP or ExperimentMode.NORM or ExperimentMode.SDP)):
                pass
            # skip if false
            else:
                index = index + 1
                option = VAMASExperimentOptions(index)
        # Optional: analysis positions
        if option == VAMASExperimentOptions.number_of_analysis_pos:
            if (self.exp_type_labels[VAMASExperimentOptions.experiment_mode]
                == (ExperimentMode.MAP or ExperimentMode.MAPDP)):
                pass
            # skip if false
            else:
                index = index + 3
                option = VAMASExperimentOptions(index)
        
        # Multiline: experimental variables
        if option == VAMASExperimentOptions.exp_variable_label and not self.second_numbered_pair:
            total_lines = self.exp_numerical_labels[VAMASExperimentOptions.number_of_exp_variables]
            index, self.exp_variables, multiline, create = self.multiline_decision(self.exp_variables, total_lines, index, 2)
            if create:
                self.VAMASExperiment[option] = []
            if multiline:
                self.second_numbered_pair = True
            option = VAMASExperimentOptions(index)
        elif option == VAMASExperimentOptions.exp_variable_label and self.second_numbered_pair:
            self.VAMASExperiment[VAMASExperimentOptions.exp_variable_unit].append(line.strip())
            self.second_numbered_pair = False

        # Multiline: manual entries
        if option == VAMASExperimentOptions.prefix_number_of_manual_entry:
            total_lines = self.exp_numerical_labels[VAMASExperimentOptions.number_of_manually_entered_items]
            index, self.manual_entries, multiline, create = self.multiline_decision(self.manual_entries, total_lines, index)
            if create:
                self.VAMASExperiment[option] = ''
            option = VAMASExperimentOptions(index)

        # Multiline: future upgrade experiment entries
        if option == VAMASExperimentOptions.future_upgrade_exp_entry:
            total_lines = self.exp_numerical_labels[VAMASExperimentOptions.number_of_future_upgrade_exp_entries]
            index, self.upgrade_exp_entries, multiline, create = self.multiline_decision(self.upgrade_exp_entries, total_lines, index)
            if create:
                self.VAMASExperiment[option] = ''
            option = VAMASExperimentOptions(index)

        if multiline:
            self.VAMASExperiment[option].append(line.strip()) 
        else:
            # add all others as normal
            self.VAMASExperiment[option] = line.strip()
            index = index + 1
            experiment_data_complete = False

            if option == VAMASExperimentOptions.number_of_blocks:
                experiment_data_complete = True
                index = 1

                for block in range(int(line.strip())):
                    self.blocks.append({})

        # add typed info to special dictionaries for future access
        if option in self.exp_numerical_labels:
            self.exp_numerical_labels[option] = int(line.strip())
        elif option == VAMASExperimentOptions.experiment_mode:
            self.exp_type_labels[option] = ExperimentMode[line.strip().upper()]
        elif option == VAMASExperimentOptions.scan_mode:
            self.exp_type_labels[option] = ScanMode[line.strip().upper()] 

        return index, experiment_data_complete

    def block_parser(self, line, index, current_block):
        '''
        line: current line of text file
        index: index into spec enum
        current_block: index of block to fill in

        returns: new index, new current_block
        '''
        block = self.blocks[current_block]

        # select the correct option from the correct enum
        # fill in header first
        if not self.current_block_header:
            option = VAMASBlockHeader(index)
            if option == VAMASBlockHeader.sample_identifier:
                self.current_block_header = True

                # initialize counters for this block
                self.block_comment_lines = 0
                self.exp_vars = 0
                self.corresponding_vars = 0
                self.additional_params = 0
                self.ordinate_vals = 0
        # then the section of numbered options
        elif not self.current_block_numbered:
            option = NumberedVAMASBlockOptions(index)

            if option == NumberedVAMASBlockOptions.comment:
                total_lines = block[NumberedVAMASBlockOptions.number_of_lines_in_comment]
                index, self.block_comment_lines, multiline, create = self.multiline_decision(self.block_comment_lines, total_lines, index)
                if create:
                    self.block[option] = []
                option = NumberedVAMASBlockOptions(index)

            if option == NumberedVAMASBlockOptions.x_coord:
                if (self.VAMASExperiment[VAMASExperimentOptions.experiment_mode]
                    == ExperimentMode.MAP or ExperimentMode.MAPDP):
                    pass 
                else:
                    index = index + 2
                    option = NumberedVAMASBlockOptions(index)

            if option == NumberedVAMASBlockOptions.value_of_experimental_variable:
                total_lines = self.VAMASExperiment[VAMASExperimentOptions.number_of_exp_variables]
                index, self.exp_vars, multiline, create = self.multiline_decision(self.exp_vars, total_lines, index)
                if create:
                    self.block[option] = []
                option = NumberedVAMASBlockOptions(index)

            if option == NumberedVAMASBlockOptions.sputtering_ion:
                if (self.VAMASExperiment[VAMASExperimentOptions.experiment_mode]
                    == ExperimentMode.MAP or ExperimentMode.MAPSV or ExperimentMode.SDP or ExperimentMode.SDPV):
                    pass 
                else:
                    index = index + 3
                    option = NumberedVAMASBlockOptions(index)     

            if option == NumberedVAMASBlockOptions.field_of_view_x:
                if (self.VAMASExperiment[VAMASExperimentOptions.experiment_mode]
                    == ExperimentMode.MAP or ExperimentMode.MAPDP or ExperimentMode.MAPSV or ExperimentMode.SEM):
                    pass 
                else:
                    index = index + 2
                    option = NumberedVAMASBlockOptions(index)       
        # finally the footer
        else:
            option = VAMASBlockFooter(index)

        if self.multiline:
            block[option].append(line.strip())
        else:
            block[option] = line.strip() 
            index = index + 1

        # TODO if statement that sets current_block += 1 if block completed
        return index, current_block

    def read_VAMAS(self):
        '''
        BASIC VAMAS FILESTRUCTURE:
            - Experiment
            - Block 1
            ...
            - Block N
        '''
        self.VAMASExperiment = {}
        self.blocks = []

        with open(self.filename) as file:
            # flags to help keep track of structure
            experiment_data_complete = False
            current_block_complete = False
            self.current_block_header = False 
            self.current_block_numbered = False 
            self.current_block_footer = False
            current_block = 0

            # counter variables
            self.comment_lines = 0
            self.exp_variables = 0
            self.entries_included = 0
            self.manual_entries = 0
            self.upgrade_exp_entries = 0

            # flags to help with variable-length options
            self.multiline = False
            self.second_numbered_pair = False

            # for indexing into Enums tracking VAMAS specs
            index = 1
            # iterate over lines in VAMAS file
            for line in file:
                # read out experiment data section
                if not experiment_data_complete:
                    index, experiment_data_complete = self.experiment_parser(line, index)
            
                elif current_block < self.exp_numerical_labels[VAMASExperimentOptions.number_of_blocks]:
                    index, current_block = self.block_parser(line, index, current_block)
                    
        return self.VAMASExperiment, self.blocks