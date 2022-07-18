import pandas as pd
import pingouin as pg
import numpy as np
from pathlib import Path
import os

import calculate_area
import utils
import data


def write_all(all_subject_data, subjects, experiment, data_directory):
    """
    Write all experiment results to experiment results text file
    Remove previous results file if exists

    Parameters
    ----------
    all_subject_data: list
        all subject data tuples
    subjects: list
        all subject IDs, based off directory names
    experiment: str
        name of experiment
    data_directory: Path
        path to all subject data directory
    """

    print(f"\n\n\nStarting {experiment} results.....\n")

    exp_result_filepath = Path(f"./results_{experiment}.txt")

    #   Remove results file if already exists
    if exp_result_filepath.exists():
        os.remove(exp_result_filepath)
        print(f"Previous results_{experiment}.txt removed\n")

    write_participant_demographics(experiment, data_directory)
    write_intercept_slope_summary(all_subject_data, experiment)
    write_example_subject_data(all_subject_data, subjects, experiment)
    write_error_and_variability_summary(all_subject_data, experiment)
    write_error_vs_variability_regression(all_subject_data, experiment)

    if experiment == "exp2":
        write_condition_vs_condition_regression(all_subject_data, experiment)
        write_low_vs_high_area_correlation(all_subject_data)
        write_low_vs_high_r2_correlation(all_subject_data)
        write_between_condition_r2_mean_difference(all_subject_data)
        write_between_condition_area_mean_difference(all_subject_data)

    if experiment == "exp1":
        write_difference_between_conditions_exp1(all_subject_data)
        write_icc_results_exp1(all_subject_data)


def write_participant_demographics(experiment, data_folder):
    age_mean, age_sd, number_females, right_handed = data._return_participant_demographics(
        experiment, data_folder
    )

    results = open(f"results_{experiment}.txt", "a")
    age = "Age mean:"
    fem = "N females:"
    right = "R handed:"
    results.write(
        f"{age:10s} {age_mean:3.1f} (SD: {age_sd:3.1f})\n{fem:10s} {number_females:10s}\n{right:10s} {right_handed:5s}\n\n"
    )
    results.close()


def write_intercept_slope_summary(all_subject_data, experiment):
    if experiment == "exp1":
        intercept_lists = [[], [], [], []]
        slope_lists = [[], [], [], []]
        condition_names = [
            "Day 1 dominant",
            "Day 1 non-dominant",
            "Day 2 dominant 1",
            "Day 2 dominant 2",
        ]
    else:
        intercept_lists = [[], [], []]
        slope_lists = [[], [], []]
        condition_names = ["Vision-to-grasp", "Grasp-to-vision", "Grasp-to-grasp"]

    for subject_data in all_subject_data:
        data_list = utils.create_data_tuples(experiment, subject_data)
        for condition_data, intercept_list, slope_list in zip(
            data_list, intercept_lists, slope_lists
        ):
            intercept, slope = utils.calculate_regression_general(
                condition_data.ACTUAL, condition_data.PERCEIVED
            )
            intercept_list.append(intercept)
            slope_list.append(slope)

    intercept_means = []
    intercept_cis = []
    slope_means = []
    slope_cis = []

    for intercept_list in intercept_lists:
        intercept_means.append(np.mean(intercept_list))
        intercept_cis.append(utils.calculate_ci(intercept_list))

    for slope_list in slope_lists:
        slope_means.append(np.mean(slope_list))
        slope_cis.append(utils.calculate_ci(slope_list))

    utils.write_result_header(experiment, "Group summary: Intercept and slope")
    utils.write_mean_ci_header(experiment)

    for condition_name, intercept_mean, intercept_ci, slope_mean, slope_ci in zip(
        condition_names, intercept_means, intercept_cis, slope_means, slope_cis
    ):
        utils.write_mean_ci_result(
            experiment, intercept_mean, intercept_ci, "intercept", condition_name
        )
        utils.write_mean_ci_result(
            experiment, slope_mean, slope_ci, "slope", condition_name
        )

    print(f"INTERCEPT and SLOPE summary results written to results_{experiment}.txt")


def write_example_subject_data(all_subject_data, subjects, experiment):
    example = utils.ExampleParticipantIDs
    if experiment == "exp1":
        subject_1_ID = example.exp1_participant_1
        subject_2_ID = example.exp1_participant_2
        condition_names = [
            "day 1 dominant",
            "day 1 non-dominant",
            "day 2 dominant 1",
            "day 2 dominant 2",
        ]
        data_list = utils.store_example_subject_data_exp1(
            all_subject_data, subjects, subject_1_ID, subject_2_ID
        )
    else:
        subject_1_ID = example.exp2_participant_1
        subject_2_ID = example.exp2_participant_2
        condition_names = ["Vision-to-grasp", "Grasp-to-vision", "Grasp-to-grasp"]
        data_list = utils.store_example_subject_data_exp2(
            all_subject_data, subjects, subject_1_ID, subject_2_ID
        )

    example_subject_names = [subject_1_ID, subject_2_ID]
    result_title = "Example participant summary"
    utils.write_result_header(experiment, result_title)

    for example_subject_data, example_subject_name in zip(
        data_list, example_subject_names
    ):
        utils.write_example_subject_name(experiment, example_subject_name)
        utils.write_example_subject_header(experiment)
        for condition_data, condition_name in zip(
            example_subject_data, condition_names
        ):
            intercept, slope = utils.calculate_regression_general(
                condition_data.ACTUAL, condition_data.PERCEIVED
            )
            area = calculate_area.normalised(
                condition_data.ACTUAL, condition_data.PERCEIVED, experiment
            )
            r2 = utils.calculate_r2(condition_data.ACTUAL, condition_data.PERCEIVED)
            utils.write_example_subject_results(
                experiment, condition_name, intercept, slope, area, r2
            )
        print(f"{example_subject_name} summary written to results_{experiment}.txt")


def write_error_and_variability_summary(all_subject_data, experiment):
    r2_means, r2_cis = utils.store_condition_r2_means_and_cis(
        all_subject_data, experiment
    )
    area_means, area_cis = calculate_area.store_condition_area_means_and_cis(
        all_subject_data, experiment
    )
    means_lists, ci_lists = [r2_means, area_means], [r2_cis, area_cis]

    results_headers = ["Variability (R^2)", "Error (cm^2 / cm)"]
    params = utils.r2_area_constants()

    result_title = "Group summary: Error and Variability"
    utils.write_result_header(experiment, result_title)
    utils.write_mean_ci_header(experiment)

    if experiment == "exp2":
        condition_names = ["Vision-to-grasp", "Grasp-to-vision", "Grasp-to-grasp"]
    else:
        condition_names = [
            "day 1 dominant",
            "day 1 non-dominant",
            "day 2 dominant 1",
            "day 2 dominant 2",
        ]

    for mean_list, ci_list, subplot, y_label in zip(
        means_lists, ci_lists, params.subplot_indices, results_headers
    ):
        for mean, ci, condition_name in zip(mean_list, ci_list, condition_names):
            utils.write_mean_ci_result(experiment, mean, ci, y_label, condition_name)

    print(f"ERROR and VARIABILITY summary written to results_{experiment}.txt")


def write_error_vs_variability_regression(all_subject_data, experiment):
    error_lists = calculate_area.area_per_exp_condition(all_subject_data, experiment)
    variability_lists = utils.store_r2_lists(all_subject_data, experiment)
    if experiment == "exp1":
        condition_names = [
            "Day 1 dominant",
            "Day 1 non-dominant",
            "Day 2 dominant 1",
            "Day 2 dominant 2",
        ]
    else:
        condition_names = ["Vision-to-grasp", "Grasp-to-vision", "Grasp-to-grasp"]

    utils.write_result_header(experiment, "Regression: Error vs. variability")

    for condition_r2_data, condition_error_data, condition_name in zip(
        variability_lists, error_lists, condition_names
    ):
        intercept, slope = utils.calculate_regression_general(
            condition_error_data, condition_r2_data
        )
        utils.write_regression_results(
            experiment,
            condition_error_data,
            condition_r2_data,
            intercept,
            slope,
            condition_name,
        )
    print(f"ERROR vs. VARIABILITY regression written to results_{experiment}.txt")


def write_condition_vs_condition_regression(all_subject_data, experiment):
    result_title = "OLS slope regression"
    condition_name = "Vision-to-grasp vs grasp-to-vision"
    utils.write_result_header(experiment, result_title)

    slopes_line_width = []
    slopes_width_line = []

    for count, subject_data in enumerate(all_subject_data, start=1):
        intercept_line_width, slope_line_width = utils.calculate_regression_general(
            subject_data.LINE_WIDTH.ACTUAL, subject_data.LINE_WIDTH.PERCEIVED
        )
        intercept_width_line, slope_width_line = utils.calculate_regression_general(
            subject_data.WIDTH_LINE.ACTUAL, subject_data.WIDTH_LINE.PERCEIVED
        )
        slopes_line_width.append(slope_line_width)
        slopes_width_line.append(slope_width_line)

    intercept, slope = utils.calculate_regression_general(
        slopes_line_width, slopes_width_line
    )

    for slope_1, slope_2 in zip(slopes_line_width, slopes_width_line):
        if slope_2 > 1.7:
            index = slopes_width_line.index(slope_2)
            slope_line_width_2 = slopes_line_width
            slope_width_line_2 = slopes_width_line
            slope_line_width_2.pop(index)
            slope_width_line_2.pop(index)
            intercept_2, slope_2 = utils.calculate_regression_general(
                slope_line_width_2, slope_width_line_2
            )

    utils.write_regression_results(
        experiment,
        slopes_line_width,
        slopes_width_line,
        intercept,
        slope,
        condition_name,
    )
    utils.write_regression_results(
        experiment,
        slope_line_width_2,
        slope_width_line_2,
        intercept_2,
        slope_2,
        "Outlier removed",
    )

    print(
        f"RECIPROCAL CONDITION OLS slope regression written to results_{experiment}.txt"
    )


def write_difference_between_conditions_exp1(all_subject_data):
    result_title = "Difference between conditions"
    experiment = "exp1"
    utils.write_result_header(experiment, result_title)
    measures = ["Error (cm^2)", "Variability (R^2)", "intercept", "slope"]
    comparison_names = ["Between hands", "Within hand", "Within hand"]
    comparison_times = ["Same day", "1 week apart", "Same day"]

    for measure in measures:
        between_hands, across_days, within_day = [], [], []
        for subject_data in all_subject_data:
            if measure == "area":
                (
                    dom_vs_non_dom,
                    dom_d1_vs_d2,
                    dom_d2_vs_d2,
                ) = calculate_area.return_condition_comparison_areas(
                    subject_data, experiment
                )
            elif measure == "intercept":
                (
                    dom_vs_non_dom,
                    dom_d1_vs_d2,
                    dom_d2_vs_d2,
                ) = utils.return_subject_between_condition_comparisons_exp1(
                    subject_data, measure
                )
            elif measure == "slope":
                (
                    dom_vs_non_dom,
                    dom_d1_vs_d2,
                    dom_d2_vs_d2,
                ) = utils.return_subject_between_condition_comparisons_exp1(
                    subject_data, measure
                )
            else:
                (
                    dom_vs_non_dom,
                    dom_d1_vs_d2,
                    dom_d2_vs_d2,
                ) = utils.return_subject_between_condition_comparisons_exp1(
                    subject_data, measure
                )

            between_hands.append(dom_vs_non_dom)
            across_days.append(dom_d1_vs_d2)
            within_day.append(dom_d2_vs_d2)

        all_difference_data = [between_hands, across_days, within_day]

        utils.write_measure_header(experiment, measure)
        utils.write_mean_ci_header("exp1")

        for data_list, name, time_period in zip(
            all_difference_data, comparison_names, comparison_times
        ):
            mean, ci = utils.calculate_mean_ci(data_list)
            utils.write_mean_ci_result(experiment, mean, ci, name, time_period)

    print(f"Difference BETWEEN CONDITIONS written in results_exp1.txt\n")


def write_icc_results_exp1(all_subject_data):
    r2_d1_dom = []
    r2_d2_dom = []
    area_d1_dom = []
    area_d2_dom = []

    for subject in all_subject_data:
        d1_dom_r2 = utils.calculate_r2(
            subject.day1_dominant.ACTUAL, subject.day1_dominant.PERCEIVED
        )
        d2_dom_r2 = utils.calculate_r2(
            subject.day2_dominant_1.ACTUAL, subject.day2_dominant_1.PERCEIVED
        )
        d1_dom_area = calculate_area.normalised(
            subject.day1_dominant.ACTUAL, subject.day1_dominant.PERCEIVED, "exp1"
        )
        d2_dom_area = calculate_area.normalised(
            subject.day2_dominant_1.ACTUAL, subject.day2_dominant_1.PERCEIVED, "exp1"
        )

        r2_d1_dom.append(d1_dom_r2)
        r2_d2_dom.append(d2_dom_r2)
        area_d1_dom.append(d1_dom_area)
        area_d2_dom.append(d2_dom_area)

    n_participants = len(all_subject_data)

    targets = _make_target_list(n_participants)
    test_session = _make_test_session_list(n_participants)

    high_r2 = r2_d1_dom + r2_d2_dom
    high_area = area_d1_dom + area_d2_dom

    high_r2_df = pd.DataFrame(
        {"targets": targets, "rater": test_session, "score": high_r2}
    )
    high_area_df = pd.DataFrame(
        {"targets": targets, "rater": test_session, "score": high_area}
    )

    high_r2_icc = pg.intraclass_corr(
        data=high_r2_df, targets="targets", raters="rater", ratings="score"
    )
    high_area_icc = pg.intraclass_corr(
        data=high_area_df, targets="targets", raters="rater", ratings="score"
    )

    high_area_icc["Outcome"] = ["Error", "Error", "Error", "Error", "Error", "Error"]
    high_r2_icc["Outcome"] = [
        "Variability",
        "Variability",
        "Variability",
        "Variability",
        "Variability",
        "Variability",
    ]

    all_ICC_values = pd.concat((high_r2_icc, high_area_icc))
    all_ICC_values.to_csv("./ICC_results_exp2.csv")

    print("ICC results exported to ./ICC_results_exp2.csv")


def _make_target_list(n_participants):
    targets = np.concatenate(
        (np.arange(1, n_participants + 1, 1), np.arange(1, n_participants + 1, 1)),
        axis=0,
    )
    targets = targets.tolist()

    return targets


def _make_test_session_list(n_participants):
    total_length = n_participants * 2
    test_session = []
    for i in range(total_length):
        if i < total_length / 2:
            test_session.append("A")
        else:
            test_session.append("B")

    return test_session


def write_low_vs_high_area_correlation(all_subject_data):
    experiment = "exp2"
    utils.write_result_header(
        experiment, "Low-level vs. High-level correlations: Error"
    )
    width_to_width_areas = []
    line_to_width_areas = []
    width_to_line_areas = []

    for participant in all_subject_data:
        width_to_width = calculate_area.normalised(
            participant.WIDTH_WIDTH.ACTUAL,
            participant.WIDTH_WIDTH.PERCEIVED,
            experiment,
        )
        line_to_width = calculate_area.normalised(
            participant.LINE_WIDTH.ACTUAL, participant.LINE_WIDTH.PERCEIVED, experiment
        )
        width_to_line = calculate_area.normalised(
            participant.WIDTH_LINE.ACTUAL, participant.WIDTH_LINE.PERCEIVED, experiment
        )

        width_to_width_areas.append(width_to_width)
        line_to_width_areas.append(line_to_width)
        width_to_line_areas.append(width_to_line)

    if (
        len(width_to_line_areas) + len(line_to_width_areas) + len(width_to_width_areas)
        != 90
    ):
        print("Uneven lists")

    utils.write_correlation(
        experiment,
        width_to_width_areas,
        line_to_width_areas,
        "Grasp-to-grasp vs Vision-to-grasp",
    )
    utils.write_correlation(
        experiment,
        width_to_width_areas,
        width_to_line_areas,
        "Grasp-to-grasp vs Grasp-to-vision",
    )
    print(
        f"Low-level vs. High-level ERROR correlations written to results_{experiment}.txt"
    )


def write_low_vs_high_r2_correlation(all_subject_data):
    width_to_width_r2 = []
    line_to_width_r2 = []
    width_to_line_r2 = []
    experiment = "exp2"

    utils.write_result_header(
        experiment, "Low-level vs. High-level correlations: Variability"
    )

    for participant in all_subject_data:
        width_to_width = utils.calculate_r2(
            participant.WIDTH_WIDTH.ACTUAL, participant.WIDTH_WIDTH.PERCEIVED
        )
        line_to_width = utils.calculate_r2(
            participant.LINE_WIDTH.ACTUAL, participant.LINE_WIDTH.PERCEIVED
        )
        width_to_line = utils.calculate_r2(
            participant.WIDTH_LINE.ACTUAL, participant.WIDTH_LINE.PERCEIVED
        )

        width_to_width_r2.append(width_to_width)
        line_to_width_r2.append(line_to_width)
        width_to_line_r2.append(width_to_line)

    if len(width_to_line_r2) + len(line_to_width_r2) + len(width_to_width_r2) != 90:
        print("Uneven lists")

    utils.write_correlation(
        experiment,
        width_to_width_r2,
        line_to_width_r2,
        "Grasp-to-grasp - Vision-to-grasp",
    )
    utils.write_correlation(
        experiment,
        width_to_width_r2,
        width_to_line_r2,
        "Grasp-to-grasp - Grasp-to-vision",
    )
    print(
        f"Low-level vs. High-level VARIABILITY correlations written to results_{experiment}.txt"
    )


def write_between_condition_r2_mean_difference(all_subject_data):
    width_to_width_r2 = []
    line_to_width_r2 = []
    width_to_line_r2 = []
    experiment = "exp2"

    utils.write_result_header(
        experiment, "Between condition mean differences: Variability"
    )

    for participant in all_subject_data:
        width_to_width = utils.calculate_r2(
            participant.WIDTH_WIDTH.ACTUAL, participant.WIDTH_WIDTH.PERCEIVED
        )
        line_to_width = utils.calculate_r2(
            participant.LINE_WIDTH.ACTUAL, participant.LINE_WIDTH.PERCEIVED
        )
        width_to_line = utils.calculate_r2(
            participant.WIDTH_LINE.ACTUAL, participant.WIDTH_LINE.PERCEIVED
        )

        width_to_width_r2.append(width_to_width)
        line_to_width_r2.append(line_to_width)
        width_to_line_r2.append(width_to_line)

    line_to_width_vs_width_to_line = [
        abs(x - y) for x, y in zip(line_to_width_r2, width_to_line_r2)
    ]
    line_to_width_vs_width_to_width = [
        abs(x - y) for x, y in zip(line_to_width_r2, width_to_width_r2)
    ]
    width_to_line_vs_width_to_width = [
        abs(x - y) for x, y in zip(width_to_line_r2, width_to_width_r2)
    ]

    lw_wl_mean, lw_wl_ci = utils.calculate_mean_ci(line_to_width_vs_width_to_line)
    lw_ww_mean, lw_ww_ci = utils.calculate_mean_ci(line_to_width_vs_width_to_width)
    wl_ww_mean, wl_ww_ci = utils.calculate_mean_ci(width_to_line_vs_width_to_width)

    utils.write_difference_mean_ci_header(experiment)
    utils.write_mean_ci_result(
        experiment, lw_wl_mean, lw_wl_ci, "Grasp-to-vision", "Vision-to-grasp  -"
    )
    utils.write_mean_ci_result(
        experiment, lw_ww_mean, lw_ww_ci, "Grasp-to-grasp", "Vision-to-grasp  -"
    )
    utils.write_mean_ci_result(
        experiment, wl_ww_mean, wl_ww_ci, "Grasp-to-grasp", "Grasp-to-vision  -"
    )
    print(
        f"Between condition VARIABILITY differences written to results_{experiment}.txt"
    )


def write_between_condition_area_mean_difference(all_subject_data):
    width_to_width_areas = []
    line_to_width_areas = []
    width_to_line_areas = []
    experiment = "exp2"

    utils.write_result_header(experiment, "Between condition mean differences: Error")

    for participant in all_subject_data:
        width_to_width = calculate_area.normalised(
            participant.WIDTH_WIDTH.ACTUAL,
            participant.WIDTH_WIDTH.PERCEIVED,
            experiment,
        )
        line_to_width = calculate_area.normalised(
            participant.LINE_WIDTH.ACTUAL, participant.LINE_WIDTH.PERCEIVED, experiment
        )
        width_to_line = calculate_area.normalised(
            participant.WIDTH_LINE.ACTUAL, participant.WIDTH_LINE.PERCEIVED, experiment
        )

        width_to_width_areas.append(width_to_width)
        line_to_width_areas.append(line_to_width)
        width_to_line_areas.append(width_to_line)

    line_to_width_vs_width_to_line = [
        abs(x - y) for x, y in zip(line_to_width_areas, width_to_line_areas)
    ]
    line_to_width_vs_width_to_width = [
        abs(x - y) for x, y in zip(line_to_width_areas, width_to_width_areas)
    ]
    width_to_line_vs_width_to_width = [
        abs(x - y) for x, y in zip(width_to_line_areas, width_to_width_areas)
    ]

    lw_wl_mean, lw_wl_ci = utils.calculate_mean_ci(line_to_width_vs_width_to_line)
    lw_ww_mean, lw_ww_ci = utils.calculate_mean_ci(line_to_width_vs_width_to_width)
    wl_ww_mean, wl_ww_ci = utils.calculate_mean_ci(width_to_line_vs_width_to_width)

    utils.write_difference_mean_ci_header(experiment)
    utils.write_mean_ci_result(
        experiment, lw_wl_mean, lw_wl_ci, "Grasp-to-vision", "Vision-to-grasp  -"
    )
    utils.write_mean_ci_result(
        experiment, lw_ww_mean, lw_ww_ci, "Grasp-to-grasp", "Vision-to-grasp  -"
    )
    utils.write_mean_ci_result(
        experiment, wl_ww_mean, wl_ww_ci, "Grasp-to-grasp", "Grasp-to-vision  -"
    )
    print(f"Between condition ERROR differences written to results_{experiment}.txt")
