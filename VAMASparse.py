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

from VAMASspecs import *
from xps.wraith.VAMAS import VAMASExperiment

def read_VAMAS(filename):
    '''
    BASIC VAMAS FILESTRUCTURE:
        - Experiment
        - Block 1
        ...
        - Block N
    '''
    experiment_numerical_metadata = dict((
        VAMASExperimentOptions.number_of_lines_in_comment,
        VAMASExperimentOptions.number_of_spectral_regions,
        VAMASExperimentOptions.number_of_exp_variables,
        VAMASExperimentOptions.number_of_entries_include_list,
        VAMASExperimentOptions.number_of_manually_entered_items,
        VAMASExperimentOptions.number_of_future_upgrade_exp_entries,
        VAMASExperimentOptions.number_of_future_upgrade_block_entries
    ))
    experiment_type_metadata = dict((
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

        index = 1
        # iterate over lines in VAMAS file
        for line in file:
            # read out experiment data section
            if not experiment_data_complete:
                # returns <VAMASExperimentOptions.NAME: index>
                option = VAMASExperimentOptions(index)
                VAMASExperiment[option.name] = line 
                
                # check for optional/multiline cases
                if option == VAMASExperimentOptions.comment:
                    # move to next option if comment length exceeded
                    if comment_lines >= experiment_numerical_metadata[VAMASExperimentOptions.number_of_lines_in_comment]:
                        index = index + 1
                        option = VAMASExperimentOptions(index)
                    # otherwise add to comment without advancing index
                    elif comment_lines == 0:
                        VAMASExperiment[option] = line.strip()
                        comment_lines = comment_lines + 1
                        continue
                    else:
                        VAMASExperiment[option] = VAMASExperiment[option] + line.strip()
                        comment_lines = comment_lines + 1
                        continue

                if option == VAMASExperimentOptions.number_of_spectral_regions:
                    if (experiment_type_metadata[VAMASExperimentOptions.experiment_mode] 
                        == (ExperimentMode.MAP or ExperimentMode.MAPDP or ExperimentMode.NORM or ExperimentMode.SDP)):
                        pass
                    # skip if false
                    else:
                        index = index + 1
                        option = VAMASExperimentOptions(index)
                if option == VAMASExperimentOptions.number_of_analysis_pos:
                    if (experiment_type_metadata[VAMASExperimentOptions.experiment_mode]
                        == (ExperimentMode.MAP or ExperimentMode.MAPDP)):
                        pass
                    # skip if false
                    else:
                        index = index + 3
                        option = VAMASExperimentOptions(index)
                
                if option == VAMASExperimentOptions.exp_variable_label:
                    if exp_variables > experiment_numerical_metadata[VAMASExperimentOptions.number_of_exp_variables]:
                        index = index + 2
                        option = VAMASExperimentOptions(index)
                    elif exp_variables == 0:
                        VAMASExperiment[option] = []
                        VAMASExperiment[option].append(line.strip())
                        exp_variables = exp_variables + 1
                        continue 
                    else:
                        VAMASExperiment[option].append(line.strip())
                        exp_variables = exp_variables + 1
                        continue 

                # add all others as normal
                VAMASExperiment[option] = line.strip()
                index = index + 1

                # add typed info to special dictionaries for future access
                if option in experiment_numerical_metadata:
                    experiment_numerical_metadata[option] = int(line.strip())
                elif option == VAMASExperimentOptions.experiment_mode:
                    experiment_type_metadata[option] = ExperimentMode[line.strip().upper()]
                elif option == VAMASExperimentOptions.scan_mode:
                    experiment_type_metadata[option] = ScanMode[line.strip().upper()] 