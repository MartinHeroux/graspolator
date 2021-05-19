import utils
from collections import namedtuple


def minimiser_area_calc(y_at_x2, y_at_x10):
    h = 8
    area = trapezium_area(y_at_x2, y_at_x10, h)
    area_difference = (48 - area)
    return area_difference


def maximiser_area_calc(y_at_x2, y_at_x10):
    h = 8
    area = trapezium_area(y_at_x2, y_at_x10, h)
    area_difference = (area - 48)
    return area_difference


def crosser_area_calc(x_intersect, y_intersect, y_at_x2, y_at_x10):
    h_left_trapezium = x_intersect - 2
    h_right_trapezium = 10 - x_intersect

    area_reality_line_left = trapezium_area(2, y_intersect, h_left_trapezium)
    area_reality_line_right = trapezium_area(y_intersect, 10, h_right_trapezium)

    area_reg_line_left = trapezium_area(y_at_x2, y_intersect, h_left_trapezium)
    area_reg_line_right = trapezium_area(y_intersect, y_at_x10, h_right_trapezium)

    if y_at_x2 < 2:
        area_left = area_reality_line_left - area_reg_line_left
        area_right = area_reg_line_right - area_reality_line_right
    else:
        area_left = area_reg_line_left - area_reality_line_left
        area_right = area_reality_line_right - area_reg_line_right

    area_difference = area_left + area_right

    return area_left, area_right, area_difference


def crosser_triangle_area_calc(x_intersect, y_intersect, y_at_x2, y_at_x10):
    h_left_shapes = x_intersect - 2
    h_right_trapezium = 10 - x_intersect

    b_length = (y_intersect + abs(y_at_x2))
    a_length_left = (2 + abs(y_at_x2))

    area_reality_line_left = trapezium_area(a_length_left, b_length, h_left_shapes)
    area_reality_line_right = trapezium_area(y_intersect, 10, h_right_trapezium)

    area_reg_line_left = triangle_area(b_length, h_left_shapes)
    area_reg_line_right = trapezium_area(y_intersect, y_at_x10, h_right_trapezium)

    area_left = area_reality_line_left - area_reg_line_left
    area_right = area_reg_line_right - area_reality_line_right

    area_difference = area_left + area_right

    return area_left, area_right, area_difference


def reg_line_crosser_area(x_intersect, y_intersect, y_at_x2_a, y_at_x10_a, y_at_x2_b, y_at_x10_b):
    h_left_trapezium = x_intersect - 2
    h_right_trapezium = 10 - x_intersect

    left_trap_area_a = trapezium_area(y_at_x2_a, y_intersect, h_left_trapezium)
    right_trap_area_a = trapezium_area(y_intersect, y_at_x10_a, h_right_trapezium)

    left_trap_area_b = trapezium_area(y_at_x2_b, y_intersect, h_left_trapezium)
    right_trap_area_b = trapezium_area(y_intersect, y_at_x10_b, h_right_trapezium)

    left_area = abs(left_trap_area_a - left_trap_area_b)
    right_area = abs(right_trap_area_a - right_trap_area_b)

    total_area = abs(left_area + right_area)
    return total_area


def reg_line_no_cross_area(y_at_x2_a, y_at_x10_a, y_at_x2_b, y_at_x10_b):
    h = 8

    area_a = trapezium_area(y_at_x2_a, y_at_x10_a, h)
    area_b = trapezium_area(y_at_x2_b, y_at_x10_b, h)

    total_area = abs(area_a - area_b)
    return total_area


def trapezium_area(a, b, h):
    a_plus_b_div_2 = (a + b) / 2
    area = a_plus_b_div_2 * h
    return area


def triangle_area(b, h):
    area = (b * h) / 2
    return area


def bh_bd_wd_areas(current_subject_data):
    Pair = namedtuple('Pair', 'data_1 data_2')

    between_hands = Pair(data_1=current_subject_data[0], data_2=current_subject_data[1])
    between_day = Pair(data_1=current_subject_data[0], data_2=current_subject_data[2])
    within_day = Pair(data_1=current_subject_data[2], data_2=current_subject_data[3])
    print('tuples created')

    between_hands_area = calculate_area(between_hands)
    between_day_area = calculate_area(between_day)
    within_day_area = calculate_area(within_day)
    print('comparison areas calculated')

    return between_hands_area, between_day_area, within_day_area


def calculate_area(data_pair):
    x_intersect, y_intersect, y_at_x2_a, y_at_x10_a, y_at_x2_b, y_at_x10_b = utils.compute_area_calc_inputs(
        data_pair)
    group = utils.subject_group_reg_lines(x_intersect)

    if group == 'cross':
        total_area = reg_line_crosser_area(x_intersect, y_intersect, y_at_x2_a, y_at_x10_a,
                                           y_at_x2_b,
                                           y_at_x10_b)
    else:
        total_area = reg_line_no_cross_area(y_at_x2_a, y_at_x10_a, y_at_x2_b, y_at_x10_b)
    return total_area


def extract_area_number(condition_data):
    intercept, slope = utils.calculate_regression(condition_data)
    x_intersect, y_intersect = utils.point_of_intersection_with_reality(intercept, slope)
    x2, x10, y_at_x2, y_at_x10 = utils.reg_line_endpoints(intercept, slope)
    group = utils.subject_group(x_intersect, y_at_x2)

    if group == 'crosser':
        area_left, area_right, area_total = crosser_area_calc(x_intersect,
                                                              y_intersect,
                                                              y_at_x2,
                                                              y_at_x10)
    elif group == 'crosser_triangle':
        area_left, area_right, area_total = crosser_triangle_area_calc(x_intersect,
                                                                       y_intersect,
                                                                       y_at_x2,
                                                                       y_at_x10)
    elif group == 'minimiser':
        area_total = minimiser_area_calc(y_at_x2, y_at_x10)
    else:
        area_total = maximiser_area_calc(y_at_x2, y_at_x10)
    return area_total
