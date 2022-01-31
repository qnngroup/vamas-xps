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

from numpy import exp
from VAMASspecs import *

def multiline_decision(current_lines, total_lines, index, lines_per_item=1):
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

def read_VAMAS(filename):
    '''
    BASIC VAMAS FILESTRUCTURE:
        - Experiment
        - Block 1
        ...
        - Block N
    '''
    experiment_numerical_metadata = dict.fromkeys((
        VAMASExperimentOptions.number_of_lines_in_comment,
        VAMASExperimentOptions.number_of_spectral_regions,
        VAMASExperimentOptions.number_of_exp_variables,
        VAMASExperimentOptions.number_of_entries_include_list,
        VAMASExperimentOptions.number_of_manually_entered_items,
        VAMASExperimentOptions.number_of_future_upgrade_exp_entries,
        VAMASExperimentOptions.number_of_future_upgrade_block_entries,
        VAMASExperimentOptions.number_of_blocks
    ))
    experiment_type_metadata = dict.fromkeys((
        VAMASExperimentOptions.experiment_mode,
        VAMASExperimentOptions.scan_mode,
    ))

    VAMASExperiment = {}
    with open(filename) as file:
        experiment_data_complete = False

        # counter variables
        comment_lines = 0
        exp_variables = 0
        entries_included = 0
        manual_entries = 0
        upgrade_exp_entries = 0

        multiline = False
        second_numbered_pair = False

        index = 1
        # iterate over lines in VAMAS file
        for line in file:
            # read out experiment data section
            if not experiment_data_complete:
                # returns <VAMASExperimentOptions.NAME: index>
                option = VAMASExperimentOptions(index)
                
                # check for optional/multiline cases
                # Multiline comment
                if option == VAMASExperimentOptions.comment:
                    total_lines = experiment_numerical_metadata[VAMASExperimentOptions.number_of_lines_in_comment]
                    index, comment_lines, multiline, create = multiline_decision(comment_lines, total_lines, index)
                    if create:
                        VAMASExperiment[option] = []
                    option = VAMASExperimentOptions(index)

                # Optional: spectral regions
                if option == VAMASExperimentOptions.number_of_spectral_regions:
                    if (experiment_type_metadata[VAMASExperimentOptions.experiment_mode] 
                        == (ExperimentMode.MAP or ExperimentMode.MAPDP or ExperimentMode.NORM or ExperimentMode.SDP)):
                        pass
                    # skip if false
                    else:
                        index = index + 1
                        option = VAMASExperimentOptions(index)
                # Optional: analysis positions
                if option == VAMASExperimentOptions.number_of_analysis_pos:
                    if (experiment_type_metadata[VAMASExperimentOptions.experiment_mode]
                        == (ExperimentMode.MAP or ExperimentMode.MAPDP)):
                        pass
                    # skip if false
                    else:
                        index = index + 3
                        option = VAMASExperimentOptions(index)
                
                # Multiline: experimental variables
                if option == VAMASExperimentOptions.exp_variable_label and not second_numbered_pair:
                    total_lines = experiment_numerical_metadata[VAMASExperimentOptions.number_of_exp_variables]
                    index, exp_variables, multiline, create = multiline_decision(exp_variables, total_lines, index, 2)
                    if create:
                        VAMASExperiment[option] = []
                    if multiline:
                        second_numbered_pair = True
                    option = VAMASExperimentOptions(index)
                elif option == VAMASExperimentOptions.exp_variable_label and second_numbered_pair:
                    VAMASExperiment[VAMASExperimentOptions.exp_variable_unit].append(line.strip())
                    second_numbered_pair = False

                # Multiline: manual entries
                if option == VAMASExperimentOptions.prefix_number_of_manual_entry:
                    total_lines = experiment_numerical_metadata[VAMASExperimentOptions.number_of_manually_entered_items]
                    index, manual_entries, multiline, create = multiline_decision(manual_entries, total_lines, index)
                    if create:
                        VAMASExperiment[option] = ''
                    option = VAMASExperimentOptions(index)

                # Multiline: future upgrade experiment entries
                if option == VAMASExperimentOptions.future_upgrade_exp_entry:
                    total_lines = experiment_numerical_metadata[VAMASExperimentOptions.number_of_future_upgrade_exp_entries]
                    index, upgrade_exp_entries, multiline, create = multiline_decision(upgrade_exp_entries, total_lines, index)
                    if create:
                        VAMASExperiment[option] = ''
                    option = VAMASExperimentOptions(index)

                if multiline:
                    VAMASExperiment[option].append(line.strip()) 
                else:
                    # add all others as normal
                    VAMASExperiment[option] = line.strip()
                    index = index + 1

                    if option == VAMASExperimentOptions.number_of_blocks:
                        experiment_data_complete = True

                # add typed info to special dictionaries for future access
                if option in experiment_numerical_metadata:
                    experiment_numerical_metadata[option] = int(line.strip())
                elif option == VAMASExperimentOptions.experiment_mode:
                    experiment_type_metadata[option] = ExperimentMode[line.strip().upper()]
                elif option == VAMASExperimentOptions.scan_mode:
                    experiment_type_metadata[option] = ScanMode[line.strip().upper()] 

    return VAMASExperiment