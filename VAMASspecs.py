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
    year = auto() # 1
    month = auto() # 2
    day = auto() # 3
    hours = auto() # 4
    minutes = auto() # 5
    seconds = auto() # 6
    number_of_hours_in_advance_of_GMT = auto() #7
    number_of_lines_in_comment = auto() #8
    # OPTIONAL - set by number_of_lines_in_comment
    comment = auto() # 8
    technique = auto() # 9
    # OPTIONAL (MAP/MAPDP), 2 lines
    x_coord = auto() # 10
    y_coord = auto() # 10
    # OPTIONAL - set by number_of_exp_variables
    value_of_experimental_variable = auto() #11
    analysis_source_label = auto() #12
    # OPTIONAL (MAPDP/MAPSVDP/SDP/SDPV or technique = FABMS/ISS/SIMS/SNMS[+ energy spec])
    sputtering_ion = auto() #13
    number_of_atoms_in_ion = auto() #13
    sputtering_ion_charge = auto() #13
    analysis_source_characteristic_energy = auto() #14
    analysis_source_strength = auto() #15
    analysis_source_beam_width_x = auto() #16
    analysis_source_beam_width_y = auto() #16
    # OPTIONAL (MAP/MAPDP/MAPSVDP/SEM)
    field_of_view_x = auto() # 17
    field_of_view_y = auto() # 17
    # OPTIONAL (MAPSV/MAPSVDP/SEM)
    first_linescan_xi = auto() # 18
    first_linescan_yi = auto() # 18
    first_linescan_xf = auto() # 18
    first_linescan_yf = auto() # 18
    last_linescan_xf = auto() # 18
    last_linescan_yf = auto() # 18
    analysis_source_polar_aoi = auto() # 19
    analysis_source_azimuth = auto() # 20
    analyzer_mode = auto() # 21
    analyzer_pass_energy = auto() # 22
    # OPTIONAL (technique = AES diff)
    differential_width = auto() # 23
    magnification_of_analyzer_transfer_lens = auto() # 24
    analyzer_work_function = auto() # 25
    target_bias = auto() # 26
    analysis_width_x = auto() # 27
    analysis_width_y = auto() # 27
    analyzer_polar_takeoff = auto() # 28
    analyzer_azimuth_takeoff = auto() # 28
    species_label = auto() # 29
    transition_state_label = auto() # 30
    charge_of_detected_particle = auto() # 30
    # OPTIONAL (scan mode = REGULAR)
    abscissa_label = auto() # 31
    abscissa_units = auto() # 31
    abscissa_start = auto() # 31
    abscissa_increment = auto() # 31
    number_of_corresponding_variables = auto() # 32
    # OPTIONAL (above > 0)
    corresponding_variable_label = auto() # 32
    corresponding_variable_units = auto() # 32
    signal_mode = auto() # 33
    signal_collection_time = auto() # 34
    number_of_scans = auto() # 35
    signal_time_correction = auto() # 36
    # OPTIONAL (technique = AES diff/AES dir/EDX/ELS/UPS/XPS/XRF AND exp = MAPDP/MAPDSVDP/SDP/SDPSV)
    sputtering_source_energy = auto() # 37
    sputtering_source_beam_current = auto() # 37
    sputtering_source_width_x = auto() # 37
    sputtering_source_width_y = auto() # 37
    sputtering_source_polar_aoi = auto() # 37
    sputtering_source_azimuth = auto() # 37
    sputtering_mode = auto() #37 # continuous or cyclic
    sample_normal_polar_tilt = auto() #38
    sample_normal_azimuth_tilt = auto() #38
    sample_rotation_angle = auto() #39
    number_of_additional_params = auto() #40
    # OPTIONAL (above > 0)
    additional_param_label = auto() # 40
    additional_param_units = auto() # 40
    additional_param_value = auto() # 40

class VAMASBlockFooter(Enum):
    # OPTIONAL (depends number_of_future_upgrade_block_entries [VAMASExperiment])
    future_upgrade_block_entry = auto()
    
    number_of_ordinate_values = auto() # = number_corresponding_variables x number of sets of corresponding vars. to be transferred
    # OPTIONAL (depends above)
    minimum_ordinate_value = auto()
    maximum_ordinate_value = auto()
    ordinate_value = auto()
