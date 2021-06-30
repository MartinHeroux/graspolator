from collections import namedtuple

import utils
from utils import calculate_regression_general


def trapezium_area(a, b, h):
    a_plus_b_div_2 = (a + b) / 2
    area = a_plus_b_div_2 * h
    return area


def triangle_area(b, h):
    area = (b * h) / 2
    return area


def between_conditions(experiment, subject_data):
    tuple_list = utils.condition_pair_tuple(experiment, subject_data)

    if experiment == 'exp1':

        dom_vs_non_dom_area = _condition_pair_area_exp1(tuple_list[0], experiment)
        dom_d1_vs_d2_area = _condition_pair_area_exp1(tuple_list[1], experiment)
        dom_d2_vs_d2_area = _condition_pair_area_exp1(tuple_list[2], experiment)

        areas = dom_vs_non_dom_area, dom_d1_vs_d2_area, dom_d2_vs_d2_area

    elif experiment == 'exp2':

        areas = _condition_pair_area_exp2(tuple_list, experiment)

    return areas


def _condition_pair_area_exp1(condition_pair_tuple, experiment):
    intercept_a, slope_a = utils.calculate_regression(condition_pair_tuple.data_1)
    intercept_b, slope_b = utils.calculate_regression(condition_pair_tuple.data_2)

    x1_x2_a, x1_x2_b, y1_y2_a, y1_y2_b = condition_pair_endpoints(condition_pair_tuple, experiment)
    intersect_x, intersect_y = _point_of_intersection_reg_lines(intercept_a, slope_a, intercept_b, slope_b)
    group = _subject_group_reg_lines_exp1(intersect_x)
    if group == 'cross':
        total_area = _reg_line_crosser_area(intersect_x, intersect_y, y1_y2_a[0], y1_y2_a[1], y1_y2_b[0], y1_y2_b[1],
                                            experiment)
    else:
        total_area = _reg_line_no_cross_area(y1_y2_a[0], y1_y2_a[1], y1_y2_b[0], y1_y2_b[1], experiment)
    return total_area


def _condition_pair_area_exp2(condition_pair_tuple, experiment):
    intercept_a, slope_a = utils.calculate_regression(condition_pair_tuple.data_1)
    intercept_b, slope_b = utils.calculate_regression(condition_pair_tuple.data_2)
    intercept_reality, slope_reality = 0, 1

    x1_x2_a, x1_x2_b, y1_y2_a, y1_y2_b = condition_pair_endpoints(condition_pair_tuple, experiment)
    x1_x2_reality, y1_y2_reality = [3, 9], [3, 9]

    intersect_x_1, intersect_y_1 = _point_of_intersection_reg_lines(intercept_a, slope_a, intercept_reality,
                                                                    slope_reality)
    intersect_x_2, intersect_y_2 = _point_of_intersection_reg_lines(intercept_b, slope_b, intercept_reality,
                                                                    slope_reality)

    area_line_first = _reg_reality_area(intersect_x_1, intersect_y_1, y1_y2_a, y1_y2_reality, experiment)
    area_width_first = _reg_reality_area(intersect_x_2, intersect_y_2, y1_y2_b, y1_y2_reality, experiment)

    areas = area_line_first, area_width_first

    return areas


def _reg_reality_area(intersection_x, intersection_y, y_coordinates_1, y_coordinates_2, experiment):
    group = _subject_group_reg_lines_exp2(intersection_x)
    if group == 'cross':
        total_area = _reg_line_crosser_area(intersection_x, intersection_y, y_coordinates_1[0], y_coordinates_1[1],
                                            y_coordinates_2[0], y_coordinates_2[1], experiment)
    else:
        total_area = _reg_line_no_cross_area(y_coordinates_1[0], y_coordinates_1[1], y_coordinates_2[0],
                                             y_coordinates_2[1], experiment)
    return total_area


def _point_of_intersection_reg_lines(intercept_a, slope_a, intercept_b, slope_b):
    m1, b1 = slope_a, intercept_a
    m2, b2 = slope_b, intercept_b
    x_intersect = (b2 - b1) / (m1 - m2)
    y_intersect = (x_intersect * slope_a) + intercept_a
    return x_intersect, y_intersect


def _subject_group_reg_lines_exp1(x_intersect):
    if 2 <= x_intersect <= 10:
        group = 'cross'
    else:
        group = 'no_cross'
    return group


def _subject_group_reg_lines_exp2(x_intersect):
    if 3 <= x_intersect <= 9:
        group = 'cross'
    else:
        group = 'no_cross'
    return group


def _reg_line_crosser_area(x_intersect, y_intersect, y_at_x2_a, y_at_x10_a, y_at_x2_b, y_at_x10_b, experiment):
    if experiment == 'exp1':
        x1 = 2
        x2 = 10
    elif experiment == 'exp2':
        x1 = 3
        x2 = 9
    else:
        print('experiment not defined reg line crosser area')

    h_left_trapezium = x_intersect - x1
    h_right_trapezium = x2 - x_intersect

    left_trap_area_a = trapezium_area(y_at_x2_a, y_intersect, h_left_trapezium)
    right_trap_area_a = trapezium_area(y_intersect, y_at_x10_a, h_right_trapezium)

    left_trap_area_b = trapezium_area(y_at_x2_b, y_intersect, h_left_trapezium)
    right_trap_area_b = trapezium_area(y_intersect, y_at_x10_b, h_right_trapezium)

    left_area = abs(left_trap_area_a - left_trap_area_b)
    right_area = abs(right_trap_area_a - right_trap_area_b)

    total_area = abs(left_area + right_area)
    return total_area


def _reg_line_no_cross_area(y_at_x2_a, y_at_x10_a, y_at_x2_b, y_at_x10_b, experiment):
    if experiment == 'exp1':
        h = 8
    elif experiment == 'exp2':
        h = 6
    else:
        print("experiment not defined reg line no cross area")

    area_a = trapezium_area(y_at_x2_a, y_at_x10_a, h)
    area_b = trapezium_area(y_at_x2_b, y_at_x10_b, h)

    total_area = abs(area_a - area_b)
    return total_area


def actual_vs_perceived(actual, perceived, experiment):
    intercept, slope = utils.calculate_regression_general(actual, perceived)
    x_intersect, y_intersect = point_of_intersection_with_reality(intercept, slope)
    x2, x10, y_at_x2, y_at_x10 = reg_line_endpoints(actual, perceived, experiment)
    group = _subject_group(x_intersect, y_at_x2, experiment)

    if group == 'crosser':
        area_left, area_right, area_total = _crosser_area_calc(x_intersect, y_intersect, y_at_x2, y_at_x10, experiment)
    elif group == 'crosser_triangle':
        area_left, area_right, area_total = _crosser_triangle_area_calc(x_intersect, y_intersect, y_at_x2, y_at_x10,
                                                                        experiment)
    elif group == 'minimiser':
        area_total = _minimiser_area_calc(y_at_x2, y_at_x10, experiment)
    else:
        area_total = _maximiser_area_calc(y_at_x2, y_at_x10, experiment)
    return abs(area_total)


def _subject_group(x_intersect, y_at_x2, experiment):
    if experiment == 'exp1':
        x1 = 2
        x2 = 10
    elif experiment == 'exp2':
        x1 = 3
        x2 = 9
    else:
        print('experiment not defined - subject group function')

    if x1 <= x_intersect <= x2 and y_at_x2 >= 0:
        group = 'crosser'
    elif x1 <= x_intersect <= x2:
        group = 'crosser_triangle'
    elif y_at_x2 >= 2:
        group = 'maximiser'
    else:
        group = 'minimiser'
    return group


def _crosser_area_calc(x_intersect, y_intersect, y_at_x2, y_at_x10, experiment):
    if experiment == 'exp1':
        x1 = 2
        x2 = 10
    elif experiment == 'exp2':
        x1 = 3
        x2 = 9
    else:
        print('experiment not defined crosser area calc')

    h_left_trapezium = x_intersect - x1
    h_right_trapezium = x2 - x_intersect

    area_reality_line_left = trapezium_area(x1, y_intersect, h_left_trapezium)
    area_reality_line_right = trapezium_area(y_intersect, x2, h_right_trapezium)

    area_reg_line_left = trapezium_area(y_at_x2, y_intersect, h_left_trapezium)
    area_reg_line_right = trapezium_area(y_intersect, y_at_x10, h_right_trapezium)

    if y_at_x2 < x1:
        area_left = area_reality_line_left - area_reg_line_left
        area_right = area_reg_line_right - area_reality_line_right
    else:
        area_left = area_reg_line_left - area_reality_line_left
        area_right = area_reality_line_right - area_reg_line_right

    area_difference = area_left + area_right

    return area_left, area_right, area_difference


def _crosser_triangle_area_calc(x_intersect, y_intersect, y_at_x2, y_at_x10, experiment):
    if experiment == 'exp1':
        x1 = 2
        x2 = 10
    elif experiment == 'exp2':
        x1 = 3
        x2 = 9
    else:
        print('experiment not defined crosser triangle area calc')

    h_left_shapes = x_intersect - x1
    h_right_trapezium = x2 - x_intersect

    b_length = (y_intersect + abs(y_at_x2))
    a_length_left = (x1 + abs(y_at_x2))

    area_reality_line_left = trapezium_area(a_length_left, b_length, h_left_shapes)
    area_reality_line_right = trapezium_area(y_intersect, x2, h_right_trapezium)

    area_reg_line_left = triangle_area(b_length, h_left_shapes)
    area_reg_line_right = trapezium_area(y_intersect, y_at_x10, h_right_trapezium)

    area_left = area_reality_line_left - area_reg_line_left
    area_right = area_reg_line_right - area_reality_line_right

    area_difference = area_left + area_right

    return area_left, area_right, area_difference


def _minimiser_area_calc(y_at_x2, y_at_x10, experiment):
    if experiment == 'exp1':
        h = 8
        whole_area = 48
    elif experiment == 'exp2':
        h = 6
        whole_area = 36
    else:
        print("experiment not defined minimiser area calc")

    area = trapezium_area(y_at_x2, y_at_x10, h)
    area_difference = (whole_area - area)
    return area_difference


def _maximiser_area_calc(y_at_x2, y_at_x10, experiment):
    if experiment == 'exp1':
        h = 8
        whole_area = 48
    elif experiment == 'exp2':
        h = 6
        whole_area = 36
    else:
        print("experiment not defined maximiser area calc")

    area = trapezium_area(y_at_x2, y_at_x10, h)
    area_difference = (area - whole_area)
    return area_difference


def condition_pair_endpoints(condition_pair_tuple, experiment):
    x1_a, x2_a, y1_a, y2_a = reg_line_endpoints(condition_pair_tuple.data_1[0], condition_pair_tuple.data_1[1],
                                                experiment)
    x1_b, x2_b, y1_b, y2_b = reg_line_endpoints(condition_pair_tuple.data_2[0], condition_pair_tuple.data_2[1],
                                                experiment)
    x1_x2_a = [x1_a, x2_a]
    x1_x2_b = [x1_b, x2_b]
    y1_y2_a = [y1_a, y2_a]
    y1_y2_b = [y1_b, y2_b]
    return x1_x2_a, x1_x2_b, y1_y2_a, y1_y2_b


def point_of_intersection_with_reality(intercept, slope):
    m1, b1 = 1, 0
    m2, b2 = slope, intercept
    x_intersect = (b2 - b1) / (m1 - m2)
    y_intersect = (x_intersect * slope) + intercept
    return x_intersect, y_intersect


def group_areas(all_subject_data, experiment):
    if experiment == 'exp1':
        area_lists_per_condition = _group_areas_exp1(all_subject_data)
    else:
        area_lists_per_condition = _group_areas_exp2(all_subject_data)

    return area_lists_per_condition


def _group_areas_exp1(all_subject_data):
    experiment = 'exp1'
    d1_dom_areas, d1_non_dom_areas, d2_dom_1_areas, d2_dom_2_areas = [], [], [], []
    area_list_tuple = namedtuple('r2s_area',
                                 'd1_dom_area_list d1_non_dom_area_list d2_dom_1_area_list d2_dom_2_area_list')

    for subject_data in all_subject_data:
        d1_dom_tuple, d1_non_dom_tuple, d2_dom_1_tuple, d2_dom_2_tuple = utils.store_index_condition_data_tuple(
            subject_data)

        d1_dom_areas.append(actual_vs_perceived(d1_dom_tuple.ACTUAL, d1_dom_tuple.PERCEIVED, experiment)),
        d1_non_dom_areas.append(actual_vs_perceived(d1_non_dom_tuple.ACTUAL, d1_non_dom_tuple.PERCEIVED, experiment)),
        d2_dom_1_areas.append(actual_vs_perceived(d2_dom_1_tuple.ACTUAL, d2_dom_1_tuple.PERCEIVED, experiment)),
        d2_dom_2_areas.append(actual_vs_perceived(d2_dom_2_tuple.ACTUAL, d2_dom_2_tuple.PERCEIVED, experiment))

    area_lists_per_condition = area_list_tuple(d1_dom_area_list=d1_dom_areas,
                                               d1_non_dom_area_list=d1_non_dom_areas,
                                               d2_dom_1_area_list=d2_dom_1_areas,
                                               d2_dom_2_area_list=d2_dom_2_areas)
    return area_lists_per_condition


def _group_areas_exp2(all_subject_data):
    experiment = 'exp2'
    line_width_areas, width_line_areas, width_width_areas = [], [], []
    area_list_tuple = namedtuple('r2s_area',
                                 'line_width_area_list width_line_area_list width_width_area_list')

    for subject_data in all_subject_data:
        data_tuples = utils.condition_plot_inputs(subject_data)

        line_width, width_line, width_width = data_tuples[0], data_tuples[1], data_tuples[2]

        line_width_areas.append(actual_vs_perceived(line_width.ACTUAL, line_width.PERCEIVED, experiment)),
        width_line_areas.append(actual_vs_perceived(width_line.ACTUAL, width_line.PERCEIVED, experiment)),
        width_width_areas.append(actual_vs_perceived(width_width.ACTUAL, width_width.PERCEIVED, experiment))

    area_lists_per_condition = area_list_tuple(line_width_area_list=line_width_areas,
                                               width_line_area_list=width_line_areas,
                                               width_width_area_list=width_width_areas)
    return area_lists_per_condition


def difference_of_difference_areas(experiment, subject_data):
    dom_vs_non_dom_area, dom_d1_vs_d2_area, d2_dom_vs_dom_area = between_conditions(experiment,
                                                                                    subject_data)
    hands_vs_day = dom_vs_non_dom_area - d2_dom_vs_dom_area
    hands_vs_days = dom_vs_non_dom_area - dom_d1_vs_d2_area
    day_vs_days = d2_dom_vs_dom_area - dom_d1_vs_d2_area
    return hands_vs_day, hands_vs_days, day_vs_days


def reg_line_endpoints(actual, perceived, experiment):
    intercept, slope = calculate_regression_general(actual, perceived)
    if experiment == 'exp1':
        x1 = 2
        x2 = 10
    elif experiment == 'exp2':
        x1 = 3
        x2 = 9
    else:
        print('experiment not defined reg line endpoints')
    y1 = slope * x1 + intercept
    y2 = slope * x2 + intercept
    return x1, x2, y1, y2


def store_area_means_CIs_per_condition(all_subject_data, experiment):
    if experiment == 'exp1':
        area_lists = _group_areas_exp1(all_subject_data)

        d1_dom_mean, d1_dom_ci = utils.calculate_mean_ci(area_lists.d1_dom_area_list)
        d1_non_dom_mean, d1_non_dom_ci = utils.calculate_mean_ci(area_lists.d1_non_dom_area_list)
        d2_dom_1_mean, d2_dom_1_ci = utils.calculate_mean_ci(area_lists.d2_dom_1_area_list)
        d2_dom_2_mean, d2_dom_2_ci = utils.calculate_mean_ci(area_lists.d2_dom_2_area_list)
        mean_list = [d1_dom_mean, d1_non_dom_mean, d2_dom_1_mean, d2_dom_2_mean]
        ci_list = [d1_dom_ci, d1_non_dom_ci, d2_dom_1_ci, d2_dom_2_ci]

    else:
        area_lists = _group_areas_exp2(all_subject_data)
        line_width_mean, line_width_ci = utils.calculate_mean_ci(area_lists.line_width_area_list)
        width_line_mean, width_line_ci = utils.calculate_mean_ci(area_lists.width_line_area_list)
        width_width_mean, width_width_ci = utils.calculate_mean_ci(area_lists.width_width_area_list)
        mean_list = [line_width_mean, width_line_mean, width_width_mean]
        ci_list = [line_width_ci, width_line_ci, width_width_ci]

    return mean_list, ci_list
