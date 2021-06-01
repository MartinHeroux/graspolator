import numpy as np
from collections import namedtuple
import matplotlib.pyplot as plt

import utils
import plot_utils
from utils import calculate_regression_general, calculate_mean_ci


def trapezium_area(a, b, h):
    a_plus_b_div_2 = (a + b) / 2
    area = a_plus_b_div_2 * h
    return area


def triangle_area(b, h):
    area = (b * h) / 2
    return area


def between_conditions(subject_data):
    dom_vs_non_dom, dom_d1_vs_d2, dom_d2_vs_d2 = plot_utils.condition_pair_tuple(subject_data)

    dom_vs_non_dom_area = _condition_pair_area(dom_vs_non_dom)
    dom_d1_vs_d2_area = _condition_pair_area(dom_d1_vs_d2)
    dom_d2_vs_d2_area = _condition_pair_area(dom_d2_vs_d2)

    return dom_vs_non_dom_area, dom_d1_vs_d2_area, dom_d2_vs_d2_area


def _condition_pair_area(condition_pair_tuple):
    intercept_a, slope_a = utils.calculate_regression(condition_pair_tuple.data_1)
    intercept_b, slope_b = utils.calculate_regression(condition_pair_tuple.data_2)

    x1_x2_a, x1_x2_b, y1_y2_a, y1_y2_b = condition_pair_endpoints(condition_pair_tuple)
    intersect_x, intersect_y = _point_of_intersection_reg_lines(intercept_a, slope_a, intercept_b, slope_b)
    group = _subject_group_reg_lines(intersect_x)
    if group == 'cross':
        total_area = _reg_line_crosser_area(intersect_x, intersect_y, y1_y2_a[0], y1_y2_a[1], y1_y2_b[0],
                                            y1_y2_b[1])
    else:
        total_area = _reg_line_no_cross_area(y1_y2_a[0], y1_y2_a[1], y1_y2_b[0], y1_y2_b[1])
    return total_area


def _point_of_intersection_reg_lines(intercept_a, slope_a, intercept_b, slope_b):
    m1, b1 = slope_a, intercept_a
    m2, b2 = slope_b, intercept_b
    x_intersect = (b2 - b1) / (m1 - m2)
    y_intersect = (x_intersect * slope_a) + intercept_a
    return x_intersect, y_intersect


def _subject_group_reg_lines(x_intersect):
    if 2 <= x_intersect <= 10:
        group = 'cross'
    else:
        group = 'no_cross'
    return group


def _reg_line_crosser_area(x_intersect, y_intersect, y_at_x2_a, y_at_x10_a, y_at_x2_b, y_at_x10_b):
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


def _reg_line_no_cross_area(y_at_x2_a, y_at_x10_a, y_at_x2_b, y_at_x10_b):
    h = 8

    area_a = trapezium_area(y_at_x2_a, y_at_x10_a, h)
    area_b = trapezium_area(y_at_x2_b, y_at_x10_b, h)

    total_area = abs(area_a - area_b)
    return total_area


def actual_vs_perceived(actual, perceived):
    intercept, slope = utils.calculate_regression_general(actual, perceived)
    x_intersect, y_intersect = point_of_intersection_with_reality(intercept, slope)
    x2, x10, y_at_x2, y_at_x10 = reg_line_endpoints(actual, perceived)
    group = _subject_group(x_intersect, y_at_x2)

    if group == 'crosser':
        area_left, area_right, area_total = _crosser_area_calc(x_intersect,
                                                               y_intersect,
                                                               y_at_x2,
                                                               y_at_x10)
    elif group == 'crosser_triangle':
        area_left, area_right, area_total = _crosser_triangle_area_calc(x_intersect,
                                                                        y_intersect,
                                                                        y_at_x2,
                                                                        y_at_x10)
    elif group == 'minimiser':
        area_total = _minimiser_area_calc(y_at_x2, y_at_x10)
    else:
        area_total = _maximiser_area_calc(y_at_x2, y_at_x10)
    return area_total


def _subject_group(x_intersect, y_at_x2):
    if 2 <= x_intersect <= 10 and y_at_x2 >= 0:
        group = 'crosser'
    elif 2 <= x_intersect <= 10:
        group = 'crosser_triangle'
    elif y_at_x2 >= 2:
        group = 'maximiser'
    else:
        group = 'minimiser'
    return group


def _crosser_area_calc(x_intersect, y_intersect, y_at_x2, y_at_x10):
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


def _crosser_triangle_area_calc(x_intersect, y_intersect, y_at_x2, y_at_x10):
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


def _minimiser_area_calc(y_at_x2, y_at_x10):
    h = 8
    area = trapezium_area(y_at_x2, y_at_x10, h)
    area_difference = (48 - area)
    return area_difference


def _maximiser_area_calc(y_at_x2, y_at_x10):
    h = 8
    area = trapezium_area(y_at_x2, y_at_x10, h)
    area_difference = (area - 48)
    return area_difference


def condition_pair_endpoints(condition_pair_tuple):
    x1_a, x2_a, y1_a, y2_a = reg_line_endpoints(condition_pair_tuple.data_1[0], condition_pair_tuple.data_1[1])
    x1_b, x2_b, y1_b, y2_b = reg_line_endpoints(condition_pair_tuple.data_2[0], condition_pair_tuple.data_2[1])
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


def abline(slope, intercept):
    """Plot a line from slope and intercept"""
    axes = plt.gca()
    x_vals = np.array(axes.get_xlim())
    y_vals = intercept + slope * x_vals
    plt.plot(x_vals, y_vals, 'k--')


def store_r2_and_area_tuples(all_subject_data, subject_IDs):
    r2s_areas = namedtuple('r2s_area',
                           'subject_ID d1_dom_r2 d1_non_dom_r2 d2_dom_1_r2 d2_dom_2_r2 d1_dom_area d1_non_dom_area '
                           'd2_dom_1_area d2_dom_2_area')
    r2_area_tuples = []

    for subject_data, subject_ID in zip(all_subject_data, subject_IDs):
        d1_dom_tuple, d1_non_dom_tuple, d2_dom_1_tuple, d2_dom_2_tuple = plot_utils.store_index_condition_data_tuple(
            subject_data)

        r2s_areas_tuple = r2s_areas(subject_ID=subject_ID,
                                    d1_dom_r2=utils.calculate_r2(d1_dom_tuple.ACTUAL, d1_dom_tuple.PERCEIVED),
                                    d1_non_dom_r2=utils.calculate_r2(d1_non_dom_tuple.ACTUAL,
                                                                     d1_non_dom_tuple.PERCEIVED),
                                    d2_dom_1_r2=utils.calculate_r2(d2_dom_1_tuple.ACTUAL, d2_dom_1_tuple.PERCEIVED),
                                    d2_dom_2_r2=utils.calculate_r2(d2_dom_2_tuple.ACTUAL, d2_dom_2_tuple.PERCEIVED),
                                    d1_dom_area=actual_vs_perceived(d1_non_dom_tuple.ACTUAL,
                                                                    d1_non_dom_tuple.PERCEIVED),
                                    d1_non_dom_area=actual_vs_perceived(d1_non_dom_tuple.ACTUAL,
                                                                        d1_non_dom_tuple.PERCEIVED),
                                    d2_dom_1_area=actual_vs_perceived(d2_dom_1_tuple.ACTUAL, d2_dom_1_tuple.PERCEIVED),
                                    d2_dom_2_area=actual_vs_perceived(d2_dom_2_tuple.ACTUAL, d2_dom_2_tuple.PERCEIVED))

        r2_area_tuples.append(r2s_areas_tuple)

    return r2_area_tuples


def group_areas(all_subject_data):
    d1_dom_areas, d1_non_dom_areas, d2_dom_1_areas, d2_dom_2_areas = [], [], [], []
    r2_area_list_tuple = namedtuple('r2s_area',
                                    'd1_dom_area_list d1_non_dom_area_list d2_dom_1_area_list d2_dom_2_area_list')

    for subject_data in all_subject_data:
        d1_dom_tuple, d1_non_dom_tuple, d2_dom_1_tuple, d2_dom_2_tuple = plot_utils.store_index_condition_data_tuple(
            subject_data)

        d1_dom_areas.append(actual_vs_perceived(d1_dom_tuple.ACTUAL, d1_dom_tuple.PERCEIVED)),
        d1_non_dom_areas.append(actual_vs_perceived(d1_non_dom_tuple.ACTUAL, d1_non_dom_tuple.PERCEIVED)),
        d2_dom_1_areas.append(actual_vs_perceived(d2_dom_1_tuple.ACTUAL, d2_dom_1_tuple.PERCEIVED)),
        d2_dom_2_areas.append(actual_vs_perceived(d2_dom_2_tuple.ACTUAL, d2_dom_2_tuple.PERCEIVED))

    area_lists_per_condition = r2_area_list_tuple(d1_dom_area_list=d1_dom_areas,
                                                  d1_non_dom_area_list=d1_non_dom_areas,
                                                  d2_dom_1_area_list=d2_dom_1_areas,
                                                  d2_dom_2_area_list=d2_dom_2_areas)
    return area_lists_per_condition


def difference_of_difference_areas(subject_data):
    dom_vs_non_dom_area, dom_d1_vs_d2_area, d2_dom_vs_dom_area = between_conditions(subject_data)
    hands_vs_day = dom_vs_non_dom_area - d2_dom_vs_dom_area
    hands_vs_days = dom_vs_non_dom_area - dom_d1_vs_d2_area
    day_vs_days = d2_dom_vs_dom_area - dom_d1_vs_d2_area
    return hands_vs_day, hands_vs_days, day_vs_days


def reg_line_endpoints(actual, perceived):
    intercept, slope = calculate_regression_general(actual, perceived)
    x1 = 2
    x2 = 10
    y1 = slope * x1 + intercept
    y2 = slope * x2 + intercept
    return x1, x2, y1, y2


def store_area_means_CIs_per_condition(all_subject_data):
    area_lists = group_areas(all_subject_data)
    d1_dom_mean, d1_dom_ci = utils.calculate_mean_ci(area_lists.d1_dom_area_list)
    d1_non_dom_mean, d1_non_dom_ci = utils.calculate_mean_ci(area_lists.d1_non_dom_area_list)
    d2_dom_1_mean, d2_dom_1_ci = utils.calculate_mean_ci(area_lists.d2_dom_1_area_list)
    d2_dom_2_mean, d2_dom_2_ci = utils.calculate_mean_ci(area_lists.d2_dom_2_area_list)
    mean_lists = [d1_dom_mean, d1_non_dom_mean, d2_dom_1_mean, d2_dom_2_mean]
    ci_lists = [d1_dom_ci, d1_non_dom_ci, d2_dom_1_ci, d2_dom_2_ci]
    return mean_lists, ci_lists