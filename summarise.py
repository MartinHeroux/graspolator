from collections import namedtuple

import numpy as np

from calculate_area import between_regression_and_reality_absolute, between_regression_and_reality_signed
from utils import store_condition_data_tuples_exp1, condition_plot_inputs, calculate_mean_ci, calculate_ci, \
    calculate_r2


def errors_per_condition(all_subject_data, experiment):
    if experiment == "exp1":
        area_lists_per_condition = all_subject_errors_exp1(all_subject_data)
    else:
        area_lists_per_condition = all_subject_errors_exp2(all_subject_data)

    return area_lists_per_condition


def all_subject_errors_exp1(all_subject_data):
    experiment = "exp1"
    d1_dom_areas, d1_non_dom_areas, d2_dom_1_areas, d2_dom_2_areas = [], [], [], []
    area_list_tuple = namedtuple(
        "r2s_area",
        "d1_dom_area_list d1_non_dom_area_list d2_dom_1_area_list d2_dom_2_area_list",
    )

    for subject_data in all_subject_data:
        (
            d1_dom_tuple,
            d1_non_dom_tuple,
            d2_dom_1_tuple,
            d2_dom_2_tuple,
        ) = store_condition_data_tuples_exp1(subject_data)

        d1_dom_areas.append(
            between_regression_and_reality_absolute(d1_dom_tuple.ACTUAL, d1_dom_tuple.PERCEIVED, experiment)
        ),
        d1_non_dom_areas.append(
            between_regression_and_reality_absolute(d1_non_dom_tuple.ACTUAL, d1_non_dom_tuple.PERCEIVED, experiment)
        ),
        d2_dom_1_areas.append(
            between_regression_and_reality_absolute(d2_dom_1_tuple.ACTUAL, d2_dom_1_tuple.PERCEIVED, experiment)
        ),
        d2_dom_2_areas.append(
            between_regression_and_reality_absolute(d2_dom_2_tuple.ACTUAL, d2_dom_2_tuple.PERCEIVED, experiment)
        )

    area_lists_per_condition = area_list_tuple(
        d1_dom_area_list=d1_dom_areas,
        d1_non_dom_area_list=d1_non_dom_areas,
        d2_dom_1_area_list=d2_dom_1_areas,
        d2_dom_2_area_list=d2_dom_2_areas,
    )
    return area_lists_per_condition


def all_subject_errors_exp2(all_subject_data):
    experiment = "exp2"
    line_width_areas, width_line_areas, width_width_areas = [], [], []
    area_list_tuple = namedtuple(
        "r2s_area", "line_width_area_list width_line_area_list width_width_area_list"
    )

    for subject_data in all_subject_data:
        data_tuples = condition_plot_inputs(subject_data)

        line_width, width_line, width_width = (
            data_tuples[0],
            data_tuples[1],
            data_tuples[2],
        )

        line_width_areas.append(
            between_regression_and_reality_absolute(line_width.ACTUAL, line_width.PERCEIVED, experiment)
        ),
        width_line_areas.append(
            between_regression_and_reality_absolute(width_line.ACTUAL, width_line.PERCEIVED, experiment)
        ),
        width_width_areas.append(
            between_regression_and_reality_absolute(width_width.ACTUAL, width_width.PERCEIVED, experiment)
        )

    area_lists_per_condition = area_list_tuple(
        line_width_area_list=line_width_areas,
        width_line_area_list=width_line_areas,
        width_width_area_list=width_width_areas,
    )
    return area_lists_per_condition


def area_mean_and_ci_by_condition(all_subject_data, experiment):
    if experiment == "exp1":
        area_lists = all_subject_errors_exp1(all_subject_data)

        d1_dom_mean, d1_dom_ci = calculate_mean_ci(area_lists.d1_dom_area_list)
        d1_non_dom_mean, d1_non_dom_ci = calculate_mean_ci(
            area_lists.d1_non_dom_area_list
        )
        d2_dom_1_mean, d2_dom_1_ci = calculate_mean_ci(
            area_lists.d2_dom_1_area_list
        )
        d2_dom_2_mean, d2_dom_2_ci = calculate_mean_ci(
            area_lists.d2_dom_2_area_list
        )
        mean_list = [d1_dom_mean, d1_non_dom_mean, d2_dom_1_mean, d2_dom_2_mean]
        ci_list = [d1_dom_ci, d1_non_dom_ci, d2_dom_1_ci, d2_dom_2_ci]

    else:
        area_lists = all_subject_errors_exp2(all_subject_data)
        line_width_mean, line_width_ci = calculate_mean_ci(
            area_lists.line_width_area_list
        )
        width_line_mean, width_line_ci = calculate_mean_ci(
            area_lists.width_line_area_list
        )
        width_width_mean, width_width_ci = calculate_mean_ci(
            area_lists.width_width_area_list
        )
        mean_list = [line_width_mean, width_line_mean, width_width_mean]
        ci_list = [line_width_ci, width_line_ci, width_width_ci]

    return mean_list, ci_list


def absolute_condition_comparison_areas(subject_data, experiment):
    d1_dom_area = between_regression_and_reality_absolute(
        subject_data.day1_dominant.ACTUAL,
        subject_data.day1_dominant.PERCEIVED,
        experiment,
    )
    d1_non_dom_area = between_regression_and_reality_absolute(
        subject_data.day1_non_dominant.ACTUAL,
        subject_data.day1_non_dominant.PERCEIVED,
        experiment,
    )
    d2_dom_1_area = between_regression_and_reality_absolute(
        subject_data.day2_dominant_1.ACTUAL,
        subject_data.day2_dominant_1.PERCEIVED,
        experiment,
    )
    d2_dom_2_area = between_regression_and_reality_absolute(
        subject_data.day2_dominant_2.ACTUAL,
        subject_data.day2_dominant_2.PERCEIVED,
        experiment,
    )

    dom_vs_non_dom_area = d1_dom_area - d1_non_dom_area

    dom_d1_vs_d2_area = d1_dom_area - d2_dom_1_area

    dom_d2_vs_d2_area = d2_dom_1_area - d2_dom_2_area

    return [dom_vs_non_dom_area, dom_d1_vs_d2_area, dom_d2_vs_d2_area]


def condition_comparison_areas(subject_data, experiment):
    d1_dom_area = between_regression_and_reality_signed(
        subject_data.day1_dominant.ACTUAL,
        subject_data.day1_dominant.PERCEIVED,
        experiment,
    )
    d1_non_dom_area = between_regression_and_reality_signed(
        subject_data.day1_non_dominant.ACTUAL,
        subject_data.day1_non_dominant.PERCEIVED,
        experiment,
    )
    d2_dom_1_area = between_regression_and_reality_signed(
        subject_data.day2_dominant_1.ACTUAL,
        subject_data.day2_dominant_1.PERCEIVED,
        experiment,
    )
    d2_dom_2_area = between_regression_and_reality_signed(
        subject_data.day2_dominant_2.ACTUAL,
        subject_data.day2_dominant_2.PERCEIVED,
        experiment,
    )

    dom_vs_non_dom_area = d1_dom_area - d1_non_dom_area

    dom_d1_vs_d2_area = d1_dom_area - d2_dom_1_area

    dom_d2_vs_d2_area = d2_dom_1_area - d2_dom_2_area

    return [dom_vs_non_dom_area, dom_d1_vs_d2_area, dom_d2_vs_d2_area]


def r2_mean_and_ci_by_condition(all_subject_data, experiment):
    r2_lists = r2_data_by_condition(all_subject_data, experiment)
    mean_list = []
    ci_list = []
    for r2_list in r2_lists:
        mean_list.append(np.mean(r2_list))
        ci_list.append(calculate_ci(r2_list))
    return mean_list, ci_list


def r2_data_by_condition(all_subject_data, experiment):
    if experiment == "exp1":
        r2_lists = _store_r2_tuples_exp1(all_subject_data)
    else:
        r2_lists = _store_r2_tuples_exp2(all_subject_data)
    return r2_lists


def _store_r2_tuples_exp1(all_subject_data):
    d1_dom_r2s, d1_non_dom_r2s, d2_dom_1_r2s, d2_dom_2_r2s = [], [], [], []
    r2_list_tuple = namedtuple(
        "r2", "d1_dom_r2_list d1_non_dom_r2_list d2_dom_1_r2_list d2_dom_2_r2_list"
    )

    for subject_data in all_subject_data:
        (
            d1_dom_tuple,
            d1_non_dom_tuple,
            d2_dom_1_tuple,
            d2_dom_2_tuple,
        ) = store_condition_data_tuples_exp1(subject_data)

        d1_dom_r2s.append(calculate_r2(d1_dom_tuple.ACTUAL, d1_dom_tuple.PERCEIVED)),
        d1_non_dom_r2s.append(
            calculate_r2(d1_non_dom_tuple.ACTUAL, d1_non_dom_tuple.PERCEIVED)
        ),
        d2_dom_1_r2s.append(
            calculate_r2(d2_dom_1_tuple.ACTUAL, d2_dom_1_tuple.PERCEIVED)
        ),
        d2_dom_2_r2s.append(
            calculate_r2(d2_dom_2_tuple.ACTUAL, d2_dom_2_tuple.PERCEIVED)
        )

    r2_tuples = r2_list_tuple(
        d1_dom_r2_list=d1_dom_r2s,
        d1_non_dom_r2_list=d1_non_dom_r2s,
        d2_dom_1_r2_list=d2_dom_1_r2s,
        d2_dom_2_r2_list=d2_dom_2_r2s,
    )
    return r2_tuples


def _store_r2_tuples_exp2(all_subject_data):
    line_width_r2s, width_line_r2s, width_width_r2s = [], [], []
    r2_list_tuple = namedtuple(
        "r2s", "line_width_r2_list width_line_r2_list, width_width_r2_list"
    )

    for subject_data in all_subject_data:
        data_tuples = condition_plot_inputs(subject_data)

        line_width, width_line, width_width = (
            data_tuples[0],
            data_tuples[1],
            data_tuples[2],
        )

        line_width_r2s.append(calculate_r2(line_width.ACTUAL, line_width.PERCEIVED)),
        width_line_r2s.append(calculate_r2(width_line.ACTUAL, width_line.PERCEIVED)),
        width_width_r2s.append(calculate_r2(width_width.ACTUAL, width_width.PERCEIVED))

    r2_tuples = r2_list_tuple(
        line_width_r2_list=line_width_r2s,
        width_line_r2_list=width_line_r2s,
        width_width_r2_list=width_width_r2s,
    )
    return r2_tuples