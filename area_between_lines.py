import regression_calcs

def area_under_line(subject_ID, subject_data):
    intercept, slope = regression_calcs.calc_reg_line_values(subject_data)
    intersection_x_value, y_when_x_is_2, y_when_x_is_10, group = subject_trapezium_points(subject_data)
    if group == 'crosser':
        area_difference = crosser_area_calc(intercept, slope, intersection_x_value, y_when_x_is_2, y_when_x_is_10)
    else:
        area_difference = minimiser_area_calc(y_when_x_is_2, y_when_x_is_10)
    return subject_ID, group, area_difference


def subject_trapezium_points(subject_data):
    intercept, slope = regression_calcs.calc_reg_line_values(subject_data)
    intersection_x_value, y_when_x_is_2, y_when_x_is_10 = regression_calcs.key_points(intercept, slope)
    group = regression_calcs.subject_group(intersection_x_value, y_when_x_is_2)
    return intersection_x_value, y_when_x_is_2, y_when_x_is_10, group


def minimiser_area_calc(y_when_x_is_2, y_when_x_is_10):
    h = 8
    area = trapezium_area(y_when_x_is_2, y_when_x_is_10, h)
    area_difference = (48 - area)
    return area_difference


def crosser_area_calc(intercept, slope, intersection_x_value, y_when_x_is_2, y_when_x_is_10):
    intersection_y_value = (slope * intersection_x_value) + intercept

    h_left_trapezium = intersection_x_value - 2
    h_right_trapezium = 10 - intersection_x_value

    area_reality_line_left = trapezium_area(2, intersection_y_value, h_left_trapezium)
    area_reality_line_right = trapezium_area(intersection_y_value, 10, h_right_trapezium)

    area_reg_line_left = trapezium_area(y_when_x_is_2, intersection_y_value, h_left_trapezium)
    area_reg_line_right = trapezium_area(intersection_y_value, y_when_x_is_10, h_right_trapezium)

    area_left = area_reality_line_left - area_reg_line_left
    area_right = area_reg_line_right - area_reality_line_right

    area_difference = area_left + area_right

    return area_difference


def trapezium_area(a, b, h):
    a_plus_b_div_2 = (a + b) / 2
    area = a_plus_b_div_2 * h
    return area

