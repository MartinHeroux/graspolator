from pathlib import Path
import copy

from scipy import stats
import numpy as np

import results_utils


def numerical(study_data: list, data_folder: Path):
    results_txt = results_utils.gen_results_txt("lovisa")
    _write_demographic_data(results_txt, "exp2", data_folder)
    _write_all_subject_outcomes(results_txt, study_data)
    plot_outcomes = _write_outcome_summary(study_data, results_txt)
    return plot_outcomes


def _write_all_subject_outcomes(results_txt, study_data):
    results_utils.write_all_subject_results_lovisa(results_txt, study_data)


def _write_demographic_data(results_txt, experiment, data_folder):
    results_utils.write_participant_demographics(results_txt, experiment, data_folder)


def _write_outcome_summary(study_data, results_txt):
    vision_to_grasp_intercept = list()
    vision_to_grasp_slope = list()
    vision_to_grasp_r_squared = list()
    vision_to_grasp_mean_abs_error = list()

    grasp_to_vision_intercept = list()
    grasp_to_vision_slope = list()
    grasp_to_vision_r_squared = list()
    grasp_to_vision_mean_abs_error = list()

    grasp_to_grasp_intercept = list()
    grasp_to_grasp_slope = list()
    grasp_to_grasp_r_squared = list()
    grasp_to_grasp_mean_abs_error = list()

    for subject_data in study_data:
        vision_to_grasp_intercept.append(subject_data.line_width.intercept)
        vision_to_grasp_slope.append(subject_data.line_width.slope)
        vision_to_grasp_r_squared.append(subject_data.line_width.r_squared)
        vision_to_grasp_mean_abs_error.append(subject_data.line_width.mean_abs_error)

        grasp_to_vision_intercept.append(subject_data.width_line.intercept)
        grasp_to_vision_slope.append(subject_data.width_line.slope)
        grasp_to_vision_r_squared.append(subject_data.width_line.r_squared)
        grasp_to_vision_mean_abs_error.append(subject_data.width_line.mean_abs_error)

        grasp_to_grasp_intercept.append(subject_data.width_width.intercept)
        grasp_to_grasp_slope.append(subject_data.width_width.slope)
        grasp_to_grasp_r_squared.append(subject_data.width_width.r_squared)
        grasp_to_grasp_mean_abs_error.append(subject_data.width_width.mean_abs_error)

    # ------------------------------------------------------------------------------------------------------------------
    # Summary of outcomes
    # ------------------------------------------------------------------------------------------------------------------

    # Intercept
    results_utils.write_result_header(results_txt, "intercept")
    results_utils.write_results_outcome_header(results_txt)

    mean, ci = results_utils.calculate_mean_ci(vision_to_grasp_intercept)
    results_utils.write_results(results_txt, "vison-to-grasp", mean, ci)

    mean, ci = results_utils.calculate_mean_ci(grasp_to_vision_intercept)
    results_utils.write_results(results_txt, "grasp-to-vision", mean, ci)

    mean, ci = results_utils.calculate_mean_ci(grasp_to_grasp_intercept)
    results_utils.write_results(results_txt, "grasp-to-grasp", mean, ci)

    # Slope
    results_utils.write_result_header(results_txt, "slope")
    results_utils.write_results_outcome_header(results_txt)

    mean, ci = results_utils.calculate_mean_ci(vision_to_grasp_slope)
    results_utils.write_results(results_txt, "vison-to-grasp", mean, ci)

    mean, ci = results_utils.calculate_mean_ci(grasp_to_vision_slope)
    results_utils.write_results(results_txt, "grasp-to-vision", mean, ci)

    mean, ci = results_utils.calculate_mean_ci(grasp_to_grasp_slope)
    results_utils.write_results(results_txt, "grasp-to-grasp", mean, ci)

    # r-squared
    results_utils.write_result_header(results_txt, "r-squared")
    results_utils.write_results_outcome_header(results_txt)

    mean, ci = results_utils.calculate_mean_ci(vision_to_grasp_r_squared)
    results_utils.write_results(results_txt, "vison-to-grasp", mean, ci)
    v_to_g_rsquared_outcomes = [mean, ci]

    mean, ci = results_utils.calculate_mean_ci(grasp_to_vision_r_squared)
    results_utils.write_results(results_txt, "grasp-to-vision", mean, ci)
    g_to_v_rsquared_outcomes = [mean, ci]

    mean, ci = results_utils.calculate_mean_ci(grasp_to_grasp_r_squared)
    results_utils.write_results(results_txt, "grasp-to-grasp", mean, ci)
    g_to_g_rsquared_outcomes = [mean, ci]

    # mean abs error
    results_utils.write_result_header(results_txt, "mean abs error")
    results_utils.write_results_outcome_header(results_txt)

    mean, ci = results_utils.calculate_mean_ci(vision_to_grasp_mean_abs_error)
    results_utils.write_results(results_txt, "vison-to-grasp", mean, ci)
    v_to_g_mae_outcomes = [mean, ci]

    mean, ci = results_utils.calculate_mean_ci(grasp_to_vision_mean_abs_error)
    results_utils.write_results(results_txt, "grasp-to-vision", mean, ci)
    g_to_v_mae_outcomes = [mean, ci]

    mean, ci = results_utils.calculate_mean_ci(grasp_to_grasp_mean_abs_error)
    results_utils.write_results(results_txt, "grasp-to-grasp", mean, ci)
    g_to_g_mae_outcomes = [mean, ci]

    # ------------------------------------------------------------------------------------------------------------------
    # Correlation: r_squared vs mean abs error
    # ------------------------------------------------------------------------------------------------------------------

    results_utils.write_result_header(
        results_txt, "Correlation: r-squared vs mean abs error"
    )
    results_utils.write_results_outcome_header(results_txt)

    vision_to_grasp_r = stats.pearsonr(
        vision_to_grasp_r_squared, vision_to_grasp_mean_abs_error
    )
    mean = vision_to_grasp_r.correlation
    ci = (
        vision_to_grasp_r.confidence_interval().low,
        vision_to_grasp_r.confidence_interval().high,
    )
    results_utils.write_results(results_txt, "vision_to_grasp", mean, ci)

    grasp_to_vision_r = stats.pearsonr(
        grasp_to_vision_r_squared, grasp_to_vision_mean_abs_error
    )
    mean = grasp_to_vision_r.correlation
    ci = (
        grasp_to_vision_r.confidence_interval().low,
        grasp_to_vision_r.confidence_interval().high,
    )
    results_utils.write_results(results_txt, "grasp_to_vision", mean, ci)

    grasp_to_grasp_r = stats.pearsonr(
        grasp_to_grasp_r_squared, grasp_to_grasp_mean_abs_error
    )
    mean = grasp_to_grasp_r.correlation
    ci = (
        grasp_to_grasp_r.confidence_interval().low,
        grasp_to_grasp_r.confidence_interval().high,
    )
    results_utils.write_results(results_txt, "grasp-to-grasp", mean, ci)

    # ------------------------------------------------------------------------------------------------------------------
    # Correlation: slope between lovisa and reverse lovisa
    # ------------------------------------------------------------------------------------------------------------------
    results_utils.write_result_header(
        results_txt, "Correlation: slope grasp-to-width vs slope width-to-grasp"
    )
    results_utils.write_results_outcome_header(results_txt)
    slope_r = stats.pearsonr(vision_to_grasp_slope, grasp_to_vision_slope)
    mean = slope_r.correlation
    ci = (slope_r.confidence_interval().low, slope_r.confidence_interval().high)
    results_utils.write_results(results_txt, "all", mean, ci)

    vg_slope = copy.deepcopy(vision_to_grasp_slope)
    gv_slope = copy.deepcopy(grasp_to_vision_slope)

    index = 0
    for i, val in enumerate(gv_slope):
        if val > 1.89:  # Identifying outlier
            index = i

    vg_slope.pop(index)
    gv_slope.pop(index)

    slope_r = stats.pearsonr(vg_slope, gv_slope)
    mean = slope_r.correlation
    ci = (slope_r.confidence_interval().low, slope_r.confidence_interval().high)
    results_utils.write_results(results_txt, "no outlier", mean, ci)

    # ------------------------------------------------------------------------------------------------------------------
    # Difference in regression between lovisa and reverse lovisa
    # ------------------------------------------------------------------------------------------------------------------
    errors = list()
    true_errors = list()
    for subject_data in study_data:
        vision_to_grasp_intercept = subject_data.line_width.intercept
        vision_to_grasp_slope_ = subject_data.line_width.slope
        min_width = np.min(subject_data.line_width.actual)
        max_width = np.max(subject_data.line_width.actual)
        grasp_to_vision_intercept = subject_data.width_line.intercept
        grasp_to_vision_slope_ = subject_data.width_line.slope

        error, true_error = results_utils.calc_diff_two_lines_relative_unity(
            inter1=vision_to_grasp_intercept,
            slope1=vision_to_grasp_slope_,
            inter2=grasp_to_vision_intercept,
            slope2=grasp_to_vision_slope_,
            min_width=min_width,
            max_width=max_width,
        )

        errors.append(error)
        true_errors.append(true_error)

    results_utils.write_result_header(
        results_txt, "Mean error between lovisa and reverse lovisa lines"
    )
    results_utils.write_results_outcome_header(results_txt)
    mean, ci = results_utils.calculate_mean_ci(errors)
    results_utils.write_results(results_txt, "", mean, ci)

    results_utils.write_result_header(
        results_txt, "Mean error between lovisa and mirrored reverse lovisa lines"
    )
    results_utils.write_results_outcome_header(results_txt)
    mean, ci = results_utils.calculate_mean_ci(true_errors)
    results_utils.write_results(results_txt, "", mean, ci)

    # ------------------------------------------------------------------------------------------------------------------
    # Difference in r-squared
    # ------------------------------------------------------------------------------------------------------------------
    results_utils.write_result_header(
        results_txt, "Difference in r-squared between conditions"
    )
    results_utils.write_results_outcome_header(results_txt)

    diff = list()
    for a, b in zip(vision_to_grasp_r_squared, grasp_to_vision_r_squared):
        diff.append(a - b)
    mean, ci = results_utils.calculate_mean_ci(diff)
    results_utils.write_results(results_txt, "vg_vs_gv", mean, ci)

    diff = list()
    for a, b in zip(vision_to_grasp_r_squared, grasp_to_grasp_r_squared):
        diff.append(a - b)
    mean, ci = results_utils.calculate_mean_ci(diff)
    results_utils.write_results(results_txt, "vg_vs_gg", mean, ci)

    diff = list()
    for a, b in zip(grasp_to_vision_r_squared, grasp_to_grasp_r_squared):
        diff.append(a - b)
    mean, ci = results_utils.calculate_mean_ci(diff)
    results_utils.write_results(results_txt, "gv_vs_gg", mean, ci)

    # ------------------------------------------------------------------------------------------------------------------
    # Difference in mean abs error
    # ------------------------------------------------------------------------------------------------------------------
    results_utils.write_result_header(
        results_txt, "Difference in mean abs error between conditions"
    )
    results_utils.write_results_outcome_header(results_txt)

    diff = list()
    for a, b in zip(vision_to_grasp_mean_abs_error, grasp_to_vision_mean_abs_error):
        diff.append(a - b)
    mean, ci = results_utils.calculate_mean_ci(diff)
    results_utils.write_results(results_txt, "vg_vs_gv", mean, ci)

    diff = list()
    for a, b in zip(vision_to_grasp_mean_abs_error, grasp_to_grasp_mean_abs_error):
        diff.append(a - b)
    mean, ci = results_utils.calculate_mean_ci(diff)
    results_utils.write_results(results_txt, "vg_vs_gg", mean, ci)

    diff = list()
    for a, b in zip(grasp_to_vision_mean_abs_error, grasp_to_grasp_mean_abs_error):
        diff.append(a - b)
    mean, ci = results_utils.calculate_mean_ci(diff)
    results_utils.write_results(results_txt, "gv_vs_gg", mean, ci)

    return (
        (
            v_to_g_rsquared_outcomes,
            g_to_v_rsquared_outcomes,
            g_to_g_rsquared_outcomes,
            v_to_g_mae_outcomes,
            g_to_v_mae_outcomes,
            g_to_g_mae_outcomes,
        ),
        (
            vision_to_grasp_r_squared,
            grasp_to_vision_r_squared,
            grasp_to_grasp_r_squared,
            vision_to_grasp_mean_abs_error,
            grasp_to_vision_mean_abs_error,
            grasp_to_grasp_mean_abs_error,
        ),
        (vision_to_grasp_slope, grasp_to_vision_slope),
    )
