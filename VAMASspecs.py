from enum import Enum, auto

class ExperimentMode(Enum):
    MAP = auto()
    MAPDP = auto()
    MAPSV = auto()
    NORM = auto()
    SDP = auto()
    SDPV = auto()
    SEM = auto()

class ScanMode(Enum):
    REGULAR = auto()
    IRREGULAR = auto()
    MAPPING = auto()

class Technique (Enum):
    AES_diff = auto()
    AES_dir = auto()
    EDX = auto()
    ELS = auto()
    FABMS = auto()
    FABMS_enspec = auto()
    ISS = auto()
    SIMS = auto()
    SIMS_enspec = auto()
    SNMS = auto()
    SNMS_enspec = auto()
    UPS = auto()
    XPS = auto()
    XRF = auto()

class VAMASExperimentOptions(Enum):
    '''
    representation of possible VAMAS experiment options
    '''
    format_identifier = auto()
    institution_identifier = auto()
    instrument_model_identifier = auto()
    operator_identifier = auto()
    experiment_identifier = auto()
    number_of_lines_in_comment = auto()
    # OPTIONAL (depends above)
    comment = auto()

    experiment_mode = auto()
    scan_mode = auto()

    # OPTIONAL (MAP/MAPDP/NORM/SDP)
    number_of_spectral_regions = auto()
    # next 3 OPTIONAL (MAP/MAPDP)
    number_of_analysis_pos = auto()
    number_of_discrete_x = auto()
    number_of_discrete_y = auto()

    number_of_exp_variables = auto()
    # OPTIONAL (depends on number_of_exp_variables)
    exp_variable_label = auto()
    exp_variable_unit = auto()
    
    number_of_entries_include_list = auto()
    # OPTIONAL (depends on number_of_entries_include_list)
    inclusion_prefix_number = auto()

    number_of_manually_entered_items = auto()
    # OPTIONAL (above)
    prefix_number_of_manual_entry = auto()

    number_of_future_upgrade_exp_entries = auto()
    number_of_future_upgrade_block_entries = auto()
    # OPTIONAL (above)
    future_upgrade_exp_entry = auto()
    
    number_of_blocks = auto()

class VAMASBlockHeader(Enum):
    block_identifier = auto()
    sample_identifier = auto()

class NumberedVAMASBlockOptions(Enum):
    '''
    representation of possible VAMAS block options
    '''
    year = 1
    month = 2
    day = 3
    hours = 4
    minutes = 5
    seconds = 6
    number_of_hours_in_advance_of_GMT = 7
    number_of_lines_in_comment = 8
    # OPTIONAL - set by number_of_lines_in_comment
    comment = 8
    technique = 9
    # OPTIONAL (MAP/MAPDP), 2 lines
    x_coord = 10
    y_coord = 10
    # OPTIONAL - set by number_of_exp_variables
    value_of_experimental_variable = 11
    analysis_source_label = 12
    # OPTIONAL (MAPDP/MAPSVDP/SDP/SDPV or technique = FABMS/ISS/SIMS/SNMS[+ energy spec])
    sputtering_ion = 13
    number_of_atoms_in_ion = 13
    sputtering_ion_charge = 13
    analysis_source_characteristic_energy = 14
    analysis_source_strength = 15
    analysis_source_beam_width_x = 16
    analysis_source_beam_width_y = 16
    # OPTIONAL (MAP/MAPDP/MAPSVDP/SEM)
    field_of_view_x = 17
    field_of_view_y = 17
    # OPTIONAL (MAPSV/MAPSVDP/SEM)
    first_linescan_xi = 18
    first_linescan_yi = 18
    first_linescan_xf = 18
    first_linescan_yf = 18
    last_linescan_xf = 18
    last_linescan_yf = 18
    analysis_source_polar_aoi = 19
    analysis_source_azimuth = 20
    analyzer_mode = 21
    analyzer_pass_energy = 22
    # OPTIONAL (technique = AES diff)
    differential_width = 23
    magnification_of_analyzer_transfer_lens = 24
    analyzer_work_function = 25
    target_bias = 26
    analysis_width_x = 27
    analysis_width_y = 27
    analyzer_polar_takeoff = 28
    analyzer_azimuth_takeoff = 28
    species_label = 29
    transition_state_label = 30
    charge_of_detected_particle = 30
    # OPTIONAL (scan mode = REGULAR)
    abscissa_label = 31
    abscissa_units = 31
    abscissa_start = 31
    abscissa_increment = 31
    number_of_corresponding_variables = 32
    # OPTIONAL (above > 0)
    corresponding_variable_label = 32
    corresponding_variable_units = 32
    signal_mode = 33
    signal_collection_time = 34
    number_of_scans = 35
    signal_time_correction = 36
    # OPTIONAL (technique = AES diff/AES dir/EDX/ELS/UPS/XPS/XRF AND exp = MAPDP/MAPDSVDP/SDP/SDPSV)
    sputtering_source_energy = 37
    sputtering_source_beam_current = 37
    sputtering_source_width_x = 37
    sputtering_source_width_y = 37
    sputtering_source_polar_aoi = 37
    sputtering_source_azimuth = 37
    sputtering_mode = 37 # continuous or cyclic
    sample_normal_polar_tilt = 38
    sample_normal_azimuth_tilt = 38
    sample_rotation_angle = 39
    number_of_additional_params = 40
    # OPTIONAL (above > 0)
    additional_param_label = 40
    additional_param_units = 40
    additional_param_value = 40

class VAMASBlockFooter(Enum):
    # OPTIONAL (depends number_of_future_upgrade_block_entries [VAMASExperiment])
    future_upgrade_block_entry = auto()
    
    number_of_ordinate_values = auto() # = number_corresponding_variables x number of sets of corresponding vars. to be transferred
    # OPTIONAL (depends above)
    minimum_ordinate_value = auto()
    maximum_ordinate_value = auto()
    ordinate_value = auto()