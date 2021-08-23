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


def normalised(actual, perceived, experiment):
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

    if experiment == 'exp1':
        normalised_area = (abs(area_total) / 8)
    elif experiment == 'exp2':
        normalised_area = (abs(area_total) / 6)

    return normalised_area


def normalised_signed(actual, perceived, experiment):
    intercept, slope = utils.calculate_regression_general(actual, perceived)
    x_intersect, y_intersect = point_of_intersection_with_reality(intercept, slope)
    x2, x10, y_at_x2, y_at_x10 = reg_line_endpoints(actual, perceived, experiment)
    group = _subject_group(x_intersect, y_at_x2, experiment)

    if group == 'crosser':
        area_total = _crosser_signed(x_intersect, y_intersect, y_at_x2, y_at_x10)
    elif group == 'crosser_triangle':
        area_total = _crosser_triangle_signed(x_intersect, y_intersect, y_at_x2, y_at_x10)
    elif group == 'minimiser':
        area_total = _minimiser_signed(y_at_x2, y_at_x10)
    else:
        area_total = _maximiser_signed(y_at_x2, y_at_x10)

    if experiment == 'exp1':
        normalised_area_signed = ((area_total) / 8)
    elif experiment == 'exp2':
        normalised_area_signed = ((area_total) / 6)

    return normalised_area_signed


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


def _minimiser_signed(y1, y2):
    h = 8
    whole_area = 48

    area = trapezium_area(y1, y2, h)
    area_total = (whole_area - area) * -1

    return area_total


def _maximiser_signed(y1, y2):
    h = 8
    whole_area = 48

    area = trapezium_area(y1, y2, h)
    area_total = (area - whole_area)
    return area_total


def _crosser_signed(x_intersect, y_intersect, y1, y2):
    x1 = 2
    x2 = 10

    h_left_trapezium = x_intersect - x1
    h_right_trapezium = x2 - x_intersect

    area_reality_line_left = trapezium_area(x1, y_intersect, h_left_trapezium)
    area_reality_line_right = trapezium_area(y_intersect, x2, h_right_trapezium)

    area_reg_line_left = trapezium_area(y1, y_intersect, h_left_trapezium)
    area_reg_line_right = trapezium_area(y_intersect, y2, h_right_trapezium)

    if y1 <= x1:
        area_left = (area_reality_line_left - area_reg_line_left) * -1
        area_right = area_reg_line_right - area_reality_line_right
    else:
        area_left = area_reg_line_left - area_reality_line_left
        area_right = (area_reality_line_right - area_reg_line_right) * -1

    area_total = area_left + area_right
    print(area_left, area_right)

    return area_total


def _crosser_triangle_signed(x_intersect, y_intersect, y1, y2):
    x1 = 2
    x2 = 10

    h_left_shapes = x_intersect - x1
    h_right_trapezium = x2 - x_intersect

    b_length = (y_intersect + abs(y1))
    a_length_left = (x1 + abs(y1))

    area_reality_line_left = trapezium_area(a_length_left, b_length, h_left_shapes)
    area_reality_line_right = trapezium_area(y_intersect, x2, h_right_trapezium)

    area_reg_line_left = triangle_area(b_length, h_left_shapes)
    area_reg_line_right = trapezium_area(y_intersect, y2, h_right_trapezium)

    area_left = (area_reality_line_left - area_reg_line_left) * -1
    area_right = area_reg_line_right - area_reality_line_right

    area_total = area_left + area_right

    return area_total


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

        d1_dom_areas.append(normalised(d1_dom_tuple.ACTUAL, d1_dom_tuple.PERCEIVED, experiment)),
        d1_non_dom_areas.append(normalised(d1_non_dom_tuple.ACTUAL, d1_non_dom_tuple.PERCEIVED, experiment)),
        d2_dom_1_areas.append(normalised(d2_dom_1_tuple.ACTUAL, d2_dom_1_tuple.PERCEIVED, experiment)),
        d2_dom_2_areas.append(normalised(d2_dom_2_tuple.ACTUAL, d2_dom_2_tuple.PERCEIVED, experiment))

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

        line_width_areas.append(normalised(line_width.ACTUAL, line_width.PERCEIVED, experiment)),
        width_line_areas.append(normalised(width_line.ACTUAL, width_line.PERCEIVED, experiment)),
        width_width_areas.append(normalised(width_width.ACTUAL, width_width.PERCEIVED, experiment))

    area_lists_per_condition = area_list_tuple(line_width_area_list=line_width_areas,
                                               width_line_area_list=width_line_areas,
                                               width_width_area_list=width_width_areas)
    return area_lists_per_condition


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


def store_condition_area_means_and_cis(all_subject_data, experiment):
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


def return_condition_comparison_areas(subject_data, experiment):
    d1_dom_area = normalised_signed(subject_data.day1_dominant.ACTUAL,
                             subject_data.day1_dominant.PERCEIVED,
                             experiment)
    d1_non_dom_area = normalised_signed(subject_data.day1_non_dominant.ACTUAL,
                                 subject_data.day1_non_dominant.PERCEIVED,
                                 experiment)
    d2_dom_1_area = normalised_signed(subject_data.day2_dominant_1.ACTUAL,
                               subject_data.day2_dominant_1.PERCEIVED,
                               experiment)
    d2_dom_2_area = normalised_signed(subject_data.day2_dominant_2.ACTUAL,
                               subject_data.day2_dominant_2.PERCEIVED,
                               experiment)

    dom_vs_non_dom_area = (d1_dom_area - d1_non_dom_area)

    dom_d1_vs_d2_area = (d1_dom_area - d2_dom_1_area)

    dom_d2_vs_d2_area = (d2_dom_1_area - d2_dom_2_area)

    return [dom_vs_non_dom_area, dom_d1_vs_d2_area, dom_d2_vs_d2_area]

