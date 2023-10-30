from pathlib import Path
import copy

from scipy import stats
import numpy as np

import results_utils
import results_lovisa


def numerical(study_data: list, data_folder: Path):
    results_txt = results_utils.gen_results_txt("kathy")
    results_lovisa._write_demographic_data(results_txt, "exp1", data_folder)
    _write_all_subject_outcomes(results_txt, study_data)
    plot_outcomes = _write_outcome_summary(study_data, results_txt)
    return plot_outcomes


def _write_all_subject_outcomes(results_txt, study_data):
    results_utils.write_all_subject_results_kathy(results_txt, study_data)


def _write_demographic_data(results_txt, experiment, data_folder):
    results_utils.write_participant_demographics(results_txt, experiment, data_folder)


def _write_outcome_summary(study_data, results_txt):
    day1_dominant_intercept = list()
    day1_dominant_slope = list()
    day1_dominant_r_squared = list()
    day1_dominant_mean_abs_error = list()

    day1_non_dominant_intercept = list()
    day1_non_dominant_slope = list()
    day1_non_dominant_r_squared = list()
    day1_non_dominant_mean_abs_error = list()

    day2_dominant_1_intercept = list()
    day2_dominant_1_slope = list()
    day2_dominant_1_r_squared = list()
    day2_dominant_1_mean_abs_error = list()

    day2_dominant_2_intercept = list()
    day2_dominant_2_slope = list()
    day2_dominant_2_r_squared = list()
    day2_dominant_2_mean_abs_error = list()

    for subject_data in study_data:
        day1_dominant_intercept.append(subject_data.day1_dominant.intercept)
        day1_dominant_slope.append(subject_data.day1_dominant.slope)
        day1_dominant_r_squared.append(subject_data.day1_dominant.r_squared)
        day1_dominant_mean_abs_error.append(subject_data.day1_dominant.mean_abs_error)

        day1_non_dominant_intercept.append(subject_data.day1_non_dominant.intercept)
        day1_non_dominant_slope.append(subject_data.day1_non_dominant.slope)
        day1_non_dominant_r_squared.append(subject_data.day1_non_dominant.r_squared)
        day1_non_dominant_mean_abs_error.append(
            subject_data.day1_non_dominant.mean_abs_error
        )

        day2_dominant_1_intercept.append(subject_data.day2_dominant_1.intercept)
        day2_dominant_1_slope.append(subject_data.day2_dominant_1.slope)
        day2_dominant_1_r_squared.append(subject_data.day2_dominant_1.r_squared)
        day2_dominant_1_mean_abs_error.append(
            subject_data.day2_dominant_1.mean_abs_error
        )

        day2_dominant_2_intercept.append(subject_data.day2_dominant_2.intercept)
        day2_dominant_2_slope.append(subject_data.day2_dominant_2.slope)
        day2_dominant_2_r_squared.append(subject_data.day2_dominant_2.r_squared)
        day2_dominant_2_mean_abs_error.append(
            subject_data.day2_dominant_2.mean_abs_error
        )

    # ------------------------------------------------------------------------------------------------------------------
    # Summary of outcomes
    # ------------------------------------------------------------------------------------------------------------------

    # Intercept
    results_utils.write_result_header(results_txt, "intercept")
    results_utils.write_results_outcome_header(results_txt)

    mean, ci = results_utils.calculate_mean_ci(day1_dominant_intercept)
    results_utils.write_results(results_txt, "day1_dominant", mean, ci)

    mean, ci = results_utils.calculate_mean_ci(day1_non_dominant_intercept)
    results_utils.write_results(results_txt, "day1_non_dominant", mean, ci)

    mean, ci = results_utils.calculate_mean_ci(day2_dominant_1_intercept)
    results_utils.write_results(results_txt, "day2_dominant_1", mean, ci)

    mean, ci = results_utils.calculate_mean_ci(day2_dominant_2_intercept)
    results_utils.write_results(results_txt, "day2_dominant_2", mean, ci)

    # Slope
    results_utils.write_result_header(results_txt, "slope")
    results_utils.write_results_outcome_header(results_txt)

    mean, ci = results_utils.calculate_mean_ci(day1_dominant_slope)
    results_utils.write_results(results_txt, "day1_dominant", mean, ci)

    mean, ci = results_utils.calculate_mean_ci(day1_non_dominant_slope)
    results_utils.write_results(results_txt, "day1_non_dominant", mean, ci)

    mean, ci = results_utils.calculate_mean_ci(day2_dominant_1_slope)
    results_utils.write_results(results_txt, "day2_dominant_1", mean, ci)

    mean, ci = results_utils.calculate_mean_ci(day2_dominant_2_slope)
    results_utils.write_results(results_txt, "day2_dominant_2", mean, ci)

    # r-squared
    results_utils.write_result_header(results_txt, "r-squared")
    results_utils.write_results_outcome_header(results_txt)

    mean, ci = results_utils.calculate_mean_ci(day1_dominant_r_squared)
    results_utils.write_results(results_txt, "day1_dominant", mean, ci)
    d1_dom_r_squared_outcomes = [mean, ci]

    mean, ci = results_utils.calculate_mean_ci(day1_non_dominant_r_squared)
    results_utils.write_results(results_txt, "day1_non_dominant", mean, ci)
    d1_non_dom_r_squared_outcomes = [mean, ci]

    mean, ci = results_utils.calculate_mean_ci(day2_dominant_1_r_squared)
    results_utils.write_results(results_txt, "day2_dominant_1", mean, ci)
    d2_dom1_r_squared_outcomes = [mean, ci]

    mean, ci = results_utils.calculate_mean_ci(day2_dominant_2_r_squared)
    results_utils.write_results(results_txt, "day2_dominant_2", mean, ci)
    d2_dom2_r_squared_outcomes = [mean, ci]

    # mean abs error
    results_utils.write_result_header(results_txt, "mean abs error")
    results_utils.write_results_outcome_header(results_txt)

    mean, ci = results_utils.calculate_mean_ci(day1_dominant_mean_abs_error)
    results_utils.write_results(results_txt, "day1_dominant", mean, ci)
    d1_dom_mae_outcomes = [mean, ci]

    mean, ci = results_utils.calculate_mean_ci(day1_non_dominant_mean_abs_error)
    results_utils.write_results(results_txt, "day1_non_dominant", mean, ci)
    d1_non_dom_mae_outcomes = [mean, ci]

    mean, ci = results_utils.calculate_mean_ci(day2_dominant_1_mean_abs_error)
    results_utils.write_results(results_txt, "day2_dominant_1", mean, ci)
    d2_dom1_mae_outcomes = [mean, ci]

    mean, ci = results_utils.calculate_mean_ci(day2_dominant_2_mean_abs_error)
    results_utils.write_results(results_txt, "day2_dominant_2", mean, ci)
    d2_dom2_mae_outcomes = [mean, ci]

    # ------------------------------------------------------------------------------------------------------------------
    # Correlation: r_squared vs mean abs error
    # ------------------------------------------------------------------------------------------------------------------

    results_utils.write_result_header(
        results_txt, "Correlation: r-squared vs mean abs error"
    )
    results_utils.write_results_outcome_header(results_txt)

    day1_dominant_r = stats.pearsonr(
        day1_dominant_r_squared, day1_dominant_mean_abs_error
    )
    mean = day1_dominant_r.correlation
    ci = (
        day1_dominant_r.confidence_interval().low,
        day1_dominant_r.confidence_interval().high,
    )
    results_utils.write_results(results_txt, "day1_dominant", mean, ci)

    day1_non_dominant_r = stats.pearsonr(
        day1_non_dominant_r_squared, day1_non_dominant_mean_abs_error
    )
    mean = day1_non_dominant_r.correlation
    ci = (
        day1_non_dominant_r.confidence_interval().low,
        day1_non_dominant_r.confidence_interval().high,
    )
    results_utils.write_results(results_txt, "day1_non_dominant", mean, ci)

    day2_dominant_1_r = stats.pearsonr(
        day2_dominant_1_r_squared, day2_dominant_1_mean_abs_error
    )
    mean = day2_dominant_1_r.correlation
    ci = (
        day2_dominant_1_r.confidence_interval().low,
        day2_dominant_1_r.confidence_interval().high,
    )
    results_utils.write_results(results_txt, "day2_dominant_2", mean, ci)

    day2_dominant_2_r = stats.pearsonr(
        day2_dominant_2_r_squared, day2_dominant_2_mean_abs_error
    )
    mean = day2_dominant_2_r.correlation
    ci = (
        day2_dominant_2_r.confidence_interval().low,
        day2_dominant_2_r.confidence_interval().high,
    )
    results_utils.write_results(results_txt, "day2_dominant_2", mean, ci)

    # ------------------------------------------------------------------------------------------------------------------
    # Difference in regression between blocks
    # ------------------------------------------------------------------------------------------------------------------
    errors1 = list()
    errors2 = list()
    errors3 = list()
    for subject_data in study_data:
        day1_dominant_intercept_ = subject_data.day1_dominant.intercept
        day1_dominant_slope_ = subject_data.day1_dominant.slope
        day1_non_dominant_intercept_ = subject_data.day1_non_dominant.intercept
        day1_non_dominant_slope_ = subject_data.day1_non_dominant.slope
        day2_dominant_1_intercept_ = subject_data.day2_dominant_1.intercept
        day2_dominant_1_slope_ = subject_data.day2_dominant_1.slope
        day2_dominant_2_intercept_ = subject_data.day2_dominant_2.intercept
        day2_dominant_2_slope_ = subject_data.day2_dominant_2.slope

        min_width = np.min(subject_data.day1_dominant.actual)
        max_width = np.max(subject_data.day1_dominant.actual)

        # D1D vs D1ND
        error1 = results_utils.calc_diff_two_lines_(
            day1_dominant_intercept_,
            day1_dominant_slope_,
            day1_non_dominant_intercept_,
            day1_non_dominant_slope_,
            min_width,
            max_width,
        )
        # D2D1 vs D2D2
        error2 = results_utils.calc_diff_two_lines_(
            day2_dominant_1_intercept_,
            day2_dominant_1_slope_,
            day2_dominant_2_intercept_,
            day2_dominant_2_slope_,
            min_width,
            max_width,
        )
        # D1D vs D1ND
        error3 = results_utils.calc_diff_two_lines_(
            day1_dominant_intercept_,
            day1_dominant_slope_,
            day2_dominant_1_intercept_,
            day2_dominant_1_slope_,
            min_width,
            max_width,
        )
        errors1.append(error1)
        errors2.append(error2)
        errors3.append(error3)

    results_utils.write_result_header(
        results_txt, "Mean absolute error D1D vs D1ND lines"
    )
    results_utils.write_results_outcome_header(results_txt)
    mean, ci = results_utils.calculate_mean_ci(errors1)
    results_utils.write_results(results_txt, "", mean, ci)
    error1_outcomes = [mean, ci]

    results_utils.write_result_header(
        results_txt, "Mean absolute error D2D1 vs D2D2 lines"
    )
    results_utils.write_results_outcome_header(results_txt)
    mean, ci = results_utils.calculate_mean_ci(errors2)
    results_utils.write_results(results_txt, "", mean, ci)
    error2_outcomes = [mean, ci]

    results_utils.write_result_header(
        results_txt, "Mean absolute error D1D vs D2D1 lines"
    )
    results_utils.write_results_outcome_header(results_txt)
    mean, ci = results_utils.calculate_mean_ci(errors3)
    results_utils.write_results(results_txt, "", mean, ci)
    error3_outcomes = [mean, ci]

    # ------------------------------------------------------------------------------------------------------------------
    # Difference in intercept
    # ------------------------------------------------------------------------------------------------------------------
    results_utils.write_result_header(
        results_txt, "Difference in r-squared between conditions"
    )
    results_utils.write_results_outcome_header(results_txt)

    diff = list()
    for a, b in zip(day1_dominant_intercept, day1_non_dominant_intercept):
        diff.append(a - b)
    mean, ci = results_utils.calculate_mean_ci(diff)
    results_utils.write_results(results_txt, "d1d_vs_d1_nd", mean, ci)
    d1d_d1nd_intercept_outcomes = [mean, ci]
    d1d_d1nd_intercept_diff = diff

    diff = list()
    for a, b in zip(day2_dominant_1_intercept, day2_dominant_2_intercept):
        diff.append(a - b)
    mean, ci = results_utils.calculate_mean_ci(diff)
    results_utils.write_results(results_txt, "d2d1_vs_d2d2", mean, ci)
    d2d1_d2d2_intercept_outcomes = [mean, ci]
    d2d1_d2d2_intercept_diff = diff

    diff = list()
    for a, b in zip(day1_dominant_intercept, day2_dominant_1_intercept):
        diff.append(a - b)
    mean, ci = results_utils.calculate_mean_ci(diff)
    results_utils.write_results(results_txt, "d1d_vs_d2d1", mean, ci)
    d1d_d2d1_intercept_outcomes = [mean, ci]
    d1d_d2d1_intercept_diff = diff

    # ------------------------------------------------------------------------------------------------------------------
    # Difference in slope
    # ------------------------------------------------------------------------------------------------------------------
    results_utils.write_result_header(
        results_txt, "Difference in slope between conditions"
    )
    results_utils.write_results_outcome_header(results_txt)

    diff = list()
    for a, b in zip(day1_dominant_slope, day1_non_dominant_slope):
        diff.append(a - b)
    mean, ci = results_utils.calculate_mean_ci(diff)
    results_utils.write_results(results_txt, "d1d_vs_d1_nd", mean, ci)
    d1d_d1nd_slope_outcomes = [mean, ci]
    d1d_d1nd_slope_diff = diff

    diff = list()
    for a, b in zip(day2_dominant_1_slope, day2_dominant_2_slope):
        diff.append(a - b)
    mean, ci = results_utils.calculate_mean_ci(diff)
    results_utils.write_results(results_txt, "d2d1_vs_d2d2", mean, ci)
    d2d1_d2d2_slope_outcomes = [mean, ci]
    d2d1_d2d2_slope_diff = diff

    diff = list()
    for a, b in zip(day1_dominant_slope, day2_dominant_1_slope):
        diff.append(a - b)
    mean, ci = results_utils.calculate_mean_ci(diff)
    results_utils.write_results(results_txt, "d1d_vs_d2d1", mean, ci)
    d1d_d2d1_slope_outcomes = [mean, ci]
    d1d_d2d1_slope_diff = diff

    # ------------------------------------------------------------------------------------------------------------------
    # Difference in r-squared
    # ------------------------------------------------------------------------------------------------------------------
    results_utils.write_result_header(
        results_txt, "Difference in r-squared between conditions"
    )
    results_utils.write_results_outcome_header(results_txt)

    diff = list()
    for a, b in zip(day1_dominant_r_squared, day1_non_dominant_r_squared):
        diff.append(a - b)
    mean, ci = results_utils.calculate_mean_ci(diff)
    results_utils.write_results(results_txt, "d1d_vs_d1_nd", mean, ci)
    d1d_d1nd_r_squared_outcomes = [mean, ci]
    d1d_d1nd_r_squared_diff = diff

    diff = list()
    for a, b in zip(day2_dominant_1_r_squared, day2_dominant_2_r_squared):
        diff.append(a - b)
    mean, ci = results_utils.calculate_mean_ci(diff)
    results_utils.write_results(results_txt, "d2d1_vs_d2d2", mean, ci)
    d2d1_d2d2_r_squared_outcomes = [mean, ci]
    d2d1_d2d2_r_squared_diff = diff

    diff = list()
    for a, b in zip(day1_dominant_r_squared, day2_dominant_1_r_squared):
        diff.append(a - b)
    mean, ci = results_utils.calculate_mean_ci(diff)
    results_utils.write_results(results_txt, "d1d_vs_d2d1", mean, ci)
    d1d_d2d1_r_squared_outcomes = [mean, ci]
    d1d_d2d1_r_squared_diff = diff

    # ------------------------------------------------------------------------------------------------------------------
    # Difference in mean absolute error
    # ------------------------------------------------------------------------------------------------------------------
    results_utils.write_result_header(
        results_txt, "Difference in mean absolute error between conditions"
    )
    results_utils.write_results_outcome_header(results_txt)

    diff = list()
    for a, b in zip(day1_dominant_mean_abs_error, day1_non_dominant_mean_abs_error):
        diff.append(a - b)
    mean, ci = results_utils.calculate_mean_ci(diff)
    results_utils.write_results(results_txt, "d1d_vs_d1_nd", mean, ci)
    d1d_d1nd_mae_outcomes = [mean, ci]
    d1d_d1nd_mae_diff = diff

    diff = list()
    for a, b in zip(day2_dominant_1_mean_abs_error, day2_dominant_2_mean_abs_error):
        diff.append(a - b)
    mean, ci = results_utils.calculate_mean_ci(diff)
    results_utils.write_results(results_txt, "d2d1_vs_d2d2", mean, ci)
    d2d1_d2d2_mae_outcomes = [mean, ci]
    d2d1_d2d2_mae_diff = diff

    diff = list()
    for a, b in zip(day1_dominant_mean_abs_error, day2_dominant_1_mean_abs_error):
        diff.append(a - b)
    mean, ci = results_utils.calculate_mean_ci(diff)
    results_utils.write_results(results_txt, "d1d_vs_d2d1", mean, ci)
    d1d_d2d1_mae_outcomes = [mean, ci]
    d1d_d2d1_mae_diff = diff

    return (
        (
            d1_dom_r_squared_outcomes,
            d1_non_dom_r_squared_outcomes,
            d2_dom1_r_squared_outcomes,
            d2_dom2_r_squared_outcomes,
            d1_dom_mae_outcomes,
            d1_non_dom_mae_outcomes,
            d2_dom1_mae_outcomes,
            d2_dom2_mae_outcomes,
        ),
        # [1] -> intercept
        (
            d1d_d1nd_intercept_outcomes,
            d1d_d1nd_intercept_diff,
            d2d1_d2d2_intercept_outcomes,
            d2d1_d2d2_intercept_diff,
            d1d_d2d1_intercept_outcomes,
            d1d_d2d1_intercept_diff,
        ),
        # [2] -> slope
        (
            d1d_d1nd_slope_outcomes,
            d1d_d1nd_slope_diff,
            d2d1_d2d2_slope_outcomes,
            d2d1_d2d2_slope_diff,
            d1d_d2d1_slope_outcomes,
            d1d_d2d1_slope_diff,
        ),
        # [3] -> r-squared
        (
            d1d_d1nd_r_squared_outcomes,
            d1d_d1nd_r_squared_diff,
            d2d1_d2d2_r_squared_outcomes,
            d2d1_d2d2_r_squared_diff,
            d1d_d2d1_r_squared_outcomes,
            d1d_d2d1_r_squared_diff,
        ),
        # [4] -> mae
        (
            d1d_d1nd_mae_outcomes,
            d1d_d1nd_mae_diff,
            d2d1_d2d2_mae_outcomes,
            d2d1_d2d2_mae_diff,
            d1d_d2d1_mae_outcomes,
            d1d_d2d1_mae_diff,
        ),
        # [5] -> error
        (error1_outcomes, errors1, error2_outcomes, errors2, error3_outcomes, errors3),
    )
