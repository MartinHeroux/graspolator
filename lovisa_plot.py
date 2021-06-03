import utils_lovisa


def scatter_and_regression(subject_ID, subject_data):
    line_width_inputs, width_line_inputs, width_width_inputs = utils_lovisa.condition_plot_inputs(subject_data)
    data_list = line_width_inputs, width_line_inputs, width_width_inputs
