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

from numpy import exp, expm1, format_float_scientific
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

        self.blocks_numerical_labels = (
            NumberedVAMASBlockOptions.number_of_lines_in_comment,
            NumberedVAMASBlockOptions.number_of_corresponding_variables,
            NumberedVAMASBlockOptions.number_of_additional_params,
            VAMASBlockFooter.number_of_ordinate_values
        )

        self.blocks_type_labels = (NumberedVAMASBlockOptions.technique)

        self.all_blocks_numerical = []
        self.all_blocks_type = []

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

    def get_x_axis(self, block_index=0):
        block = self.blocks[block_index]
        block_numerical_labels = self.blocks[block_index]

        label = block[NumberedVAMASBlockOptions.abscissa_label]
        units = block[NumberedVAMASBlockOptions.abscissa_units]
        start = float(block[NumberedVAMASBlockOptions.abscissa_start])
        increment = float(block[NumberedVAMASBlockOptions.abscissa_increment])

        x = []
        for i in range(block_numerical_labels[VAMASBlockFooter.number_of_ordinate_values]):
            x.append(start + increment*i)
        return x, label, units

    def get_ordinate_vals(self, variable_index, block_index=0):
        '''
        variable_index: index of the corresponding variable for values of interest
        block_index: index of block to read

        returns a list of values associated with the corresponding variable
        at variable_index
        '''
        data = self.get_block_data(VAMASBlockFooter.ordinate_value, block_index)
        return data[variable_index]

    def get_corresponding_var_label(self, variable_index, block_index = 0):
        '''
        variable_index: index of the corresponding variable to read label from
        block_index: index of block to read

        returns a string -- the name of the corresponding variable
        at variable_index
        '''
        data = self.get_block_data(NumberedVAMASBlockOptions.corresponding_variable_label, block_index)
        return data[variable_index]

    def get_experiment_data(self, option):
        return self.VAMASExperiment[option]

    def get_block_data(self, option, block_index=0):
        return self.blocks[block_index][option]

    def experiment_parser(self, line, index):
        '''
        line = line of file to be read
        index = current index into Experiment spec enum

        Reads line into the appropriate key of self.VAMASExperiment (dictionary)

        returns new index & Boolean representing whether the Experiment data is all read
        '''
        option = VAMASExperimentOptions(index)
        multiline = False
        experiment_data_complete = False
                    
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
                in (ExperimentMode.MAP, ExperimentMode.MAPDP, ExperimentMode.NORM, ExperimentMode.SDP)):
                pass
            # skip if false
            else:
                index = index + 1
                option = VAMASExperimentOptions(index)

        # Optional: analysis positions
        if option == VAMASExperimentOptions.number_of_analysis_pos:
            if (self.exp_type_labels[VAMASExperimentOptions.experiment_mode]
                in (ExperimentMode.MAP, ExperimentMode.MAPDP)):
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

        # Multiline: entries_include/exclude_list
        if option == VAMASExperimentOptions.inclusion_prefix_number:
            total_lines = self.exp_numerical_labels[VAMASExperimentOptions.number_of_entries_include_list]
            index, self.entries_included, multiline, create = self.multiline_decision(self.entries_included, total_lines, index)
            if create:
                self.VAMASExperiment[option] = []
            option = VAMASExperimentOptions(index)

        # Multiline: manual entries
        if option == VAMASExperimentOptions.prefix_number_of_manual_entry:
            total_lines = self.exp_numerical_labels[VAMASExperimentOptions.number_of_manually_entered_items]
            index, self.manual_entries, multiline, create = self.multiline_decision(self.manual_entries, total_lines, index)
            if create:
                self.VAMASExperiment[option] = []
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
                    self.all_blocks_numerical.append(dict.fromkeys(self.blocks_numerical_labels))
                    self.all_blocks_type.append({NumberedVAMASBlockOptions.technique:None})

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
        block_numerical_labels = self.all_blocks_numerical[current_block]
        block_type_labels = self.all_blocks_type[current_block]
        multiline = False

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
                self.upgrade_blocks = 0
                self.ordinate_val_labels = 0
                self.ordinate_vals = 0

                self.third_numbered_pair = False
                index = 0
        # then the section of numbered options
        
        elif not self.current_block_numbered:
            option = NumberedVAMASBlockOptions(index)

            # MUTLILINE: number_of_lines_in_comment
            if option == NumberedVAMASBlockOptions.comment:
                total_lines = block_numerical_labels[NumberedVAMASBlockOptions.number_of_lines_in_comment]
                index, self.block_comment_lines, multiline, create = self.multiline_decision(self.block_comment_lines, total_lines, index)
                if create:
                    block[option] = []
                option = NumberedVAMASBlockOptions(index)

            # OPTIONAL: ExperimentMode = MAP/MAPDP
            if option == NumberedVAMASBlockOptions.x_coord:
                if (self.exp_type_labels[VAMASExperimentOptions.experiment_mode]
                    in (ExperimentMode.MAP, ExperimentMode.MAPDP)):
                    pass
                else:
                    index = index + 2
                    option = NumberedVAMASBlockOptions(index)

            # MULTILINE: number_of_exp_variables
            if option == NumberedVAMASBlockOptions.value_of_experimental_variable:
                total_lines = self.exp_numerical_labels[VAMASExperimentOptions.number_of_exp_variables]
                index, self.exp_vars, multiline, create = self.multiline_decision(self.exp_vars, total_lines, index)
                if create:
                    block[option] = []
                option = NumberedVAMASBlockOptions(index)

            # OPTIONAL: ExperimentMode = MAP/MAPSVDP/SDP/SDPSV
            if option == NumberedVAMASBlockOptions.sputtering_ion:
                if (self.exp_type_labels[VAMASExperimentOptions.experiment_mode]
                    in (ExperimentMode.MAP, ExperimentMode.MAPSVDP, ExperimentMode.SDP, ExperimentMode.SDPSV)):
                    pass 
                else:
                    index = index + 3
                    option = NumberedVAMASBlockOptions(index)     

            # OPTIONAL: ExperimentMode = MAP/MAPDP/MAPSV/SEM
            if option == NumberedVAMASBlockOptions.field_of_view_x:
                if (self.exp_type_labels[VAMASExperimentOptions.experiment_mode]
                    in (ExperimentMode.MAP, ExperimentMode.MAPDP, 
                    ExperimentMode.MAPSV, ExperimentMode.SEM)):
                    pass 
                else:
                    index = index + 2
                    option = NumberedVAMASBlockOptions(index)    

            # OPTIONAL: ExperimentMode = MAPSV/MAPSVDP/SEM
            if option == NumberedVAMASBlockOptions.first_linescan_xi:
                if (self.exp_type_labels[VAMASExperimentOptions.experiment_mode]
                    in (ExperimentMode.MAPSV, ExperimentMode.MAPSVDP, ExperimentMode.SEM)):   
                    pass
                else:
                    index = index + 6
                    option = NumberedVAMASBlockOptions(index)
            
            # OPTIONAL: Technique = AES_diff
            if option == NumberedVAMASBlockOptions.differential_width:
                if (block_type_labels[NumberedVAMASBlockOptions.technique]
                    == Technique.AES_diff):
                    pass 
                else:
                    index = index + 1
                    option = NumberedVAMASBlockOptions(index)

            # OPTIONAL: ScanMode = REGULAR
            if option == NumberedVAMASBlockOptions.abscissa_label:
                if (self.exp_type_labels[VAMASExperimentOptions.scan_mode]
                    == ScanMode.REGULAR):
                    pass 
                else:
                    index = index + 4
                    option = NumberedVAMASBlockOptions(index)

            # MULTILINE: number_of_corresponding_variables
            if option == NumberedVAMASBlockOptions.corresponding_variable_label and not self.second_numbered_pair:
                total_lines = block_numerical_labels[NumberedVAMASBlockOptions.number_of_corresponding_variables]
                index, self.corresponding_vars, multiline, create = self.multiline_decision(self.corresponding_vars, total_lines, index, 2)
                if create:
                    block[option] = []
                    block[NumberedVAMASBlockOptions.corresponding_variable_units] = []
                if multiline:
                    self.second_numbered_pair = True
                option = NumberedVAMASBlockOptions(index)
            elif option == NumberedVAMASBlockOptions.corresponding_variable_label and self.second_numbered_pair:
                block[NumberedVAMASBlockOptions.corresponding_variable_units].append(line.strip())
                self.second_numbered_pair = False
                return index, current_block

            # OPTIONAL: Technique = AES_diff/AES_dir/EDX/ELS AND ExperimentMode = MAPDP/MAPSVDP/SDP/SDPSV
            if option == NumberedVAMASBlockOptions.sputtering_source_energy:
                if (block_type_labels[NumberedVAMASBlockOptions.technique]
                    in (Technique.AES_diff, Technique.AES_dir, Technique.EDX, Technique.ELS,
                     Technique.UPS, Technique.XPS, Technique.XRF)
                    and self.exp_type_labels[VAMASExperimentOptions.experiment_mode]
                    in (ExperimentMode.MAPDP, ExperimentMode.MAPSVDP, ExperimentMode.SDP, 
                     ExperimentMode.SDPSV)):
                    pass 
                else:
                    index = index + 7
                    option = NumberedVAMASBlockOptions(index)

            # MUTLILINE: number_of_additional_params
            if option == NumberedVAMASBlockOptions.additional_param_label and not (self.second_numbered_pair or self.third_numbered_pair):
                total_lines = block_numerical_labels[NumberedVAMASBlockOptions.number_of_additional_params]
                index, self.additional_params, multiline, create = self.multiline_decision(self.additional_params, total_lines, index, 3)
                if create:
                    block[option] = []
                    block[NumberedVAMASBlockOptions.additional_param_units] = []
                    block[NumberedVAMASBlockOptions.additional_param_value] = []
                if multiline:
                    self.second_numbered_pair = True
                    self.third_numbered_pair = True 
                else:
                    self.current_block_numbered = True
                    index = 1
                option = NumberedVAMASBlockOptions(index)
            elif option == NumberedVAMASBlockOptions.additional_param_label and self.second_numbered_pair:
                block[NumberedVAMASBlockOptions.additional_param_units].append(line.strip())
                self.second_numbered_pair = False 
                return index, current_block
            elif option == NumberedVAMASBlockOptions.additional_param_label and self.third_numbered_pair:
                block[NumberedVAMASBlockOptions.additional_param_value].append(line.strip())
                self.third_numbered_pair = False
                return index, current_block

        # finally the footer
        if self.current_block_numbered:
            option = VAMASBlockFooter(index)

            # MULTILINE: number_of_future_upgrade_block_entries
            if option == VAMASBlockFooter.future_upgrade_block_entry:
                total_lines = self.exp_numerical_labels[VAMASExperimentOptions.number_of_future_upgrade_block_entries]
                index, self.upgrade_blocks, multiline, create = self.multiline_decision(self.upgrade_blocks, total_lines, index)
                if create:
                    block[option] = []
                option = VAMASBlockFooter(index)

            # MUTLILINE: number_of_corresponding_variables
            if option == VAMASBlockFooter.minimum_ordinate_value and not self.second_numbered_pair:
                total_lines = block_numerical_labels[NumberedVAMASBlockOptions.number_of_corresponding_variables]
                index, self.ordinate_val_labels, multiline, create = self.multiline_decision(self.ordinate_val_labels, total_lines, index, 2)
                if create:
                    block[option] = []
                    block[VAMASBlockFooter.maximum_ordinate_value] = []
                if multiline:
                    self.second_numbered_pair = True
                option = VAMASBlockFooter(index)
            elif option == VAMASBlockFooter.minimum_ordinate_value and self.second_numbered_pair:
                block[VAMASBlockFooter.maximum_ordinate_value].append(line.strip())
                self.second_numbered_pair = False 
                return index, current_block

            # !!! THIS IS THE DATA !!!
            if option == VAMASBlockFooter.ordinate_value:
                total_lines = block_numerical_labels[VAMASBlockFooter.number_of_ordinate_values]
                lines_per_item = block_numerical_labels[NumberedVAMASBlockOptions.number_of_corresponding_variables]

                index, self.ordinate_vals, multiline, create = self.multiline_decision(self.ordinate_vals, total_lines, index, lines_per_item)
                # create a list for the values in each variable
                if create:
                    self.var_index = 0
                    block[VAMASBlockFooter.ordinate_value] = []
                    for var in range(lines_per_item):
                        block[VAMASBlockFooter.ordinate_value].append([])

                if self.var_index >= lines_per_item:
                    self.var_index = 0


        # populate control dictionaries
        if option in block_numerical_labels:
            block_numerical_labels[option] = int(line.strip())
        elif option == NumberedVAMASBlockOptions.technique:
            block_type_labels[NumberedVAMASBlockOptions.technique] == Technique[line.strip().upper()]

        if multiline and option == VAMASBlockFooter.ordinate_value:
            block[option][self.var_index].append(float(line.strip()))
            self.var_index = self.var_index + 1
        elif multiline:
            block[option].append(line.strip())
        elif option == VAMASBlockFooter.ordinate_value:
            self.current_block_footer = True 
        else:
            block[option] = line.strip() 
            index = index + 1

        if self.current_block_footer:
            current_block = current_block + 1 

            self.current_block_header = False 
            self.current_block_numbered = False 
            self.current_block_footer = False

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