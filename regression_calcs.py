import utils


def subject_reg_line(subject_data):
    intercept, slope = calc_reg_line_values(subject_data)
    intersection_x_value, y_when_x_is_2, y_when_x_is_10 = key_points(intercept, slope)
    line_colour = subject_line_colour(intersection_x_value, y_when_x_is_2)
    return y_when_x_is_2, y_when_x_is_10, line_colour


def calc_reg_line_values(subject_data):
    # TODO: discuss if preferred option is to plot the regression for each day,
    #  instead of the combined data set for each participant
    actual_widths = []
    perceived_widths = []
    for block in subject_data:
        actual_widths.append(block.actual_widths)
        perceived_widths.append(block.perceived_widths)
    for actual, perceived in zip(actual_widths, perceived_widths):
        intercept, slope = utils.calculate_regression_all_data(actual, perceived)
    return intercept, slope


def key_points(intercept, slope):
    m1, b1 = 1, 0
    m2, b2 = slope, intercept
    x_point_of_intersection = (b2 - b1) / (m1 - m2)
    y_value_when_x_equals_2 = (2 * slope) + intercept
    y_value_when_x_equals_10 = (10 * slope) + intercept
    return x_point_of_intersection, y_value_when_x_equals_2, y_value_when_x_equals_10


def subject_line_colour(intersection_x_value, y_when_x_equals_2):
    if intersection_x_value >= 2 and intersection_x_value <= 10:
        line_colour = 'royalblue'
    elif y_when_x_equals_2 > 2:
        line_colour = 'green'
    else:
        line_colour = 'firebrick'
    return line_colour

def subject_group(intersection_x_value, y_when_x_equals_2):
    if intersection_x_value >= 2 and intersection_x_value <= 10:
        group = 'crosser'
    elif y_when_x_equals_2 > 2:
        group = 'maximiser'
    else:
        group = 'minimiser'
    return group