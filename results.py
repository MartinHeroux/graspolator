import numpy as np
from pathlib import Path
import os

import calculate_area
import summarise
import utils
import data

LOVISA = "exp2"

KATHY = "exp1"

results_savepath = utils.create_results_save_path()


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
    manuscript_experiment: str
        name of experiment
    data_directory: Path
        path to all subject data directory
    """

    if experiment == 'exp1':
        manuscript_experiment = 'exp2'
    else:
        manuscript_experiment = 'exp1'

    chronological_experiment = experiment

    exp_result_filepath = Path(results_savepath, f"results_{manuscript_experiment}.txt")

    #   Remove results file if already exists
    if exp_result_filepath.exists():
        os.remove(exp_result_filepath)
        print(f"Previous results_{manuscript_experiment}.txt removed\n")

    print(f'Starting to write to {exp_result_filepath}.\n')

    write_participant_demographics(manuscript_experiment, chronological_experiment, data_directory)
    write_intercept_slope_summary(all_subject_data, chronological_experiment, manuscript_experiment)
    write_example_subject_data(all_subject_data, subjects, chronological_experiment, manuscript_experiment)
    write_error_and_variability_summary(all_subject_data, chronological_experiment, manuscript_experiment)
    write_error_vs_variability_regression(all_subject_data, chronological_experiment, manuscript_experiment)

    if manuscript_experiment == "exp1":
        write_condition_vs_condition_regression(all_subject_data, chronological_experiment, manuscript_experiment)
        write_low_vs_high_area_correlation(all_subject_data)
        write_low_vs_high_r2_correlation(all_subject_data)
        write_between_condition_r2_mean_difference(all_subject_data)
        write_between_condition_area_mean_difference(all_subject_data)

    if manuscript_experiment == "exp2":
        write_difference_between_conditions_exp1(all_subject_data)

    print(f'Finished writing to {exp_result_filepath}.\n')


def write_participant_demographics(manuscript_experiment, chronological_experiment, data_folder):
    age_mean, age_sd, number_females, right_handed = data._return_participant_demographics(
        chronological_experiment, data_folder
    )

    results = open(f"./results/results_{manuscript_experiment}.txt", "a")
    age = "Age mean:"
    fem = "N females:"
    right = "R handed:"
    results.write(
        f"{age:10s} {age_mean:3.1f} (SD: {age_sd:3.1f})\n{fem:10s} {number_females:10s}\n{right:10s} {right_handed:5s}\n\n"
    )
    results.close()


def write_intercept_slope_summary(all_subject_data, chronological_experiment, manuscript_experiment):
    if chronological_experiment == KATHY:
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
        data_list = utils.create_data_tuples(chronological_experiment, subject_data)
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

    utils.write_result_header(manuscript_experiment, "Group summary: Intercept and slope")
    utils.write_mean_ci_header(manuscript_experiment)

    for condition_name, intercept_mean, intercept_ci, slope_mean, slope_ci in zip(
        condition_names, intercept_means, intercept_cis, slope_means, slope_cis
    ):
        utils.write_mean_ci_result(
            manuscript_experiment, intercept_mean, intercept_ci, "intercept", condition_name
        )
        utils.write_mean_ci_result(
            manuscript_experiment, slope_mean, slope_ci, "slope", condition_name
        )

    print(f"INTERCEPT + SLOPE SUMMARY written")


def write_example_subject_data(all_subject_data, subjects, chronological_experiment, manuscript_experiment):
    example = utils.ExampleParticipantIDs
    if chronological_experiment == KATHY:
        subject_1_ID = example.exp1_participant_1
        subject_2_ID = example.exp1_participant_2
        condition_names = [
            "day 1 dominant",
            "day 1 non-dominant",
            "day 2 dominant 1",
            "day 2 dominant 2",
        ]
        data_list = utils.store_example_subject_data_kathy(
            all_subject_data, subjects, subject_1_ID, subject_2_ID
        )
    else:
        subject_1_ID = example.exp2_participant_1
        subject_2_ID = example.exp2_participant_2
        condition_names = ["Vision-to-grasp", "Grasp-to-vision", "Grasp-to-grasp"]
        data_list = utils.store_example_subject_data_lovisa(
            all_subject_data, subjects, subject_1_ID, subject_2_ID
        )

    example_subject_names = [subject_1_ID, subject_2_ID]
    result_title = "Example participant summary"
    utils.write_result_header(manuscript_experiment, result_title)

    for example_subject_data, example_subject_name in zip(
        data_list, example_subject_names
    ):
        utils.write_example_subject_name(manuscript_experiment, example_subject_name)
        utils.write_example_subject_header(manuscript_experiment)
        for condition_data, condition_name in zip(
            example_subject_data, condition_names
        ):
            intercept, slope = utils.calculate_regression_general(
                condition_data.ACTUAL, condition_data.PERCEIVED
            )
            area = calculate_area.between_regression_and_reality_absolute(
                condition_data.ACTUAL, condition_data.PERCEIVED, chronological_experiment
            )
            r2 = utils.calculate_r2(condition_data.ACTUAL, condition_data.PERCEIVED)
            utils.write_example_subject_results(
                manuscript_experiment, condition_name, intercept, slope, area, r2
            )
        print(f"{example_subject_name} summary written.")


def write_error_and_variability_summary(all_subject_data, chronological_experiment, manuscript_experiment):
    r2_means, r2_cis = summarise.r2_mean_and_ci_by_condition(
        all_subject_data, chronological_experiment
    )
    area_means, area_cis = summarise.area_mean_and_ci_by_condition(
        all_subject_data, chronological_experiment
    )
    means_lists, ci_lists = [r2_means, area_means], [r2_cis, area_cis]

    results_headers = ["Variability (R^2)", "Error (cm^2 / cm)"]
    params = utils.r2_area_constants()

    result_title = "Group summary: Error and Variability"
    utils.write_result_header(manuscript_experiment, result_title)
    utils.write_mean_ci_header(manuscript_experiment)

    if chronological_experiment == LOVISA:
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
            utils.write_mean_ci_result(manuscript_experiment, mean, ci, y_label, condition_name)

    print(f"ERROR and VARIABILITY summary written.")


def write_error_vs_variability_regression(all_subject_data, chronological_experiment, manuscript_experiment):
    error_lists = summarise.errors_per_condition(all_subject_data, chronological_experiment)
    variability_lists = summarise.r2_data_by_condition(all_subject_data, chronological_experiment)
    if chronological_experiment == KATHY:
        condition_names = [
            "Day 1 dominant",
            "Day 1 non-dominant",
            "Day 2 dominant 1",
            "Day 2 dominant 2",
        ]
    else:
        condition_names = ["Vision-to-grasp", "Grasp-to-vision", "Grasp-to-grasp"]

    utils.write_result_header(manuscript_experiment, "Regression: Error vs. variability")

    for condition_r2_data, condition_error_data, condition_name in zip(
        variability_lists, error_lists, condition_names
    ):
        intercept, slope = utils.calculate_regression_general(
            condition_error_data, condition_r2_data
        )
        utils.write_regression_results(
            manuscript_experiment,
            condition_error_data,
            condition_r2_data,
            intercept,
            slope,
            condition_name,
        )
    print(f"ERROR vs. VARIABILITY regression written.")


def write_condition_vs_condition_regression(all_subject_data, chronological_experiment, manuscript_experiment):
    result_title = "OLS slope regression"
    condition_name = "Vision-to-grasp vs grasp-to-vision"
    utils.write_result_header(manuscript_experiment, result_title)

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
        manuscript_experiment,
        slopes_line_width,
        slopes_width_line,
        intercept,
        slope,
        condition_name,
    )
    utils.write_regression_results(
        manuscript_experiment,
        slope_line_width_2,
        slope_width_line_2,
        intercept_2,
        slope_2,
        "Outlier removed",
    )

    print(
        f"RECIPROCAL CONDITION SLOPE REGRESSION written."
    )


def write_difference_between_conditions_exp1(all_subject_data):
    result_title = "Difference between conditions"
    experiment = KATHY
    utils.write_result_header('exp2', result_title)
    measures = ["area", "R2", "intercept", "slope"]
    measure_labels = ["Error (cm^2)", "Variability (R^2)", "intercept", "slope"]
    comparison_names = ["Between hands", "Within hand", "Within hand"]
    comparison_times = ["Same day", "1 week apart", "Same day"]

    for measure, measure_label in zip(measures, measure_labels):
        between_hands, across_days, within_day = [], [], []
        for subject_data in all_subject_data:
            if measure == "area":
                (
                    dom_vs_non_dom,
                    dom_d1_vs_d2,
                    dom_d2_vs_d2,
                ) = summarise.absolute_condition_comparison_areas(
                    subject_data, experiment
                )
            elif measure == "intercept":
                (
                    dom_vs_non_dom,
                    dom_d1_vs_d2,
                    dom_d2_vs_d2,
                ) = utils.return_subject_between_condition_comparisons_kathy(
                    subject_data, measure
                )
            elif measure == "slope":
                (
                    dom_vs_non_dom,
                    dom_d1_vs_d2,
                    dom_d2_vs_d2,
                ) = utils.return_subject_between_condition_comparisons_kathy(
                    subject_data, measure
                )
            else:
                (
                    dom_vs_non_dom,
                    dom_d1_vs_d2,
                    dom_d2_vs_d2,
                ) = utils.return_subject_between_condition_comparisons_kathy(
                    subject_data, measure
                )

            between_hands.append(dom_vs_non_dom)
            across_days.append(dom_d1_vs_d2)
            within_day.append(dom_d2_vs_d2)

        all_difference_data = [between_hands, across_days, within_day]

        utils.write_measure_header('exp2', measure_label)
        utils.write_mean_ci_header('exp2')

        for data_list, name, time_period in zip(
            all_difference_data, comparison_names, comparison_times
        ):
            mean, ci = utils.calculate_mean_ci(data_list)
            utils.write_mean_ci_result('exp2', mean, ci, name, time_period)

    print(f"DIFFERENCE BETWEEN CONDITIONS written.")



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
    experiment = LOVISA
    utils.write_result_header(
        'exp1', "Low-level vs. High-level correlations: Error"
    )
    width_to_width_areas = []
    line_to_width_areas = []
    width_to_line_areas = []

    for participant in all_subject_data:
        width_to_width = calculate_area.between_regression_and_reality_absolute(
            participant.WIDTH_WIDTH.ACTUAL,
            participant.WIDTH_WIDTH.PERCEIVED,
            experiment,
        )
        line_to_width = calculate_area.between_regression_and_reality_absolute(
            participant.LINE_WIDTH.ACTUAL, participant.LINE_WIDTH.PERCEIVED, experiment
        )
        width_to_line = calculate_area.between_regression_and_reality_absolute(
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
        'exp1',
        width_to_width_areas,
        line_to_width_areas,
        "Grasp-to-grasp vs Vision-to-grasp",
    )
    utils.write_correlation(
        'exp1',
        width_to_width_areas,
        width_to_line_areas,
        "Grasp-to-grasp vs Grasp-to-vision",
    )
    print(
        f"CORRELATION LOW-LEVEL vs HIGH-LEVEL ERROR written."
    )


def write_low_vs_high_r2_correlation(all_subject_data):
    width_to_width_r2 = []
    line_to_width_r2 = []
    width_to_line_r2 = []
    experiment = LOVISA

    utils.write_result_header(
        'exp1', "Low-level vs. High-level correlations: Variability"
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
        'exp1',
        width_to_width_r2,
        line_to_width_r2,
        "Grasp-to-grasp vs. Vision-to-grasp",
    )
    utils.write_correlation(
        'exp1',
        width_to_width_r2,
        width_to_line_r2,
        "Grasp-to-grasp vs. Grasp-to-vision",
    )
    print(
        f"CORRELATION LOW-LEVEL VS HIGH_LEVEL VARIABILITY written."
    )


def write_between_condition_r2_mean_difference(all_subject_data):
    width_to_width_r2 = []
    line_to_width_r2 = []
    width_to_line_r2 = []
    experiment = LOVISA

    utils.write_result_header(
        'exp1', "Between condition mean differences: Variability"
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
        x - y for x, y in zip(line_to_width_r2, width_to_line_r2)
    ]
    line_to_width_vs_width_to_width = [
        x - y for x, y in zip(line_to_width_r2, width_to_width_r2)
    ]
    width_to_line_vs_width_to_width = [
        x - y for x, y in zip(width_to_line_r2, width_to_width_r2)
    ]


    lw_wl_mean, lw_wl_ci = utils.calculate_mean_ci(line_to_width_vs_width_to_line)
    lw_ww_mean, lw_ww_ci = utils.calculate_mean_ci(line_to_width_vs_width_to_width)
    wl_ww_mean, wl_ww_ci = utils.calculate_mean_ci(width_to_line_vs_width_to_width)

    utils.write_difference_mean_ci_header('exp1')
    utils.write_mean_ci_result(
        'exp1', lw_wl_mean, lw_wl_ci, "Grasp-to-vision", "Vision-to-grasp  -"
    )
    utils.write_mean_ci_result(
        'exp1', lw_ww_mean, lw_ww_ci, "Grasp-to-grasp", "Vision-to-grasp  -"
    )
    utils.write_mean_ci_result(
        'exp1', wl_ww_mean, wl_ww_ci, "Grasp-to-grasp", "Grasp-to-vision  -"
    )
    print(
        f"BETWEEN CONDITION DIFFERENCE - VARIABILITY written."
    )


def write_between_condition_area_mean_difference(all_subject_data):
    width_to_width_areas = []
    line_to_width_areas = []
    width_to_line_areas = []
    experiment = LOVISA

    utils.write_result_header('exp1', "Between condition mean differences: Error")

    for participant in all_subject_data:
        width_to_width = calculate_area.between_regression_and_reality_absolute(
            participant.WIDTH_WIDTH.ACTUAL,
            participant.WIDTH_WIDTH.PERCEIVED,
            experiment,
        )
        line_to_width = calculate_area.between_regression_and_reality_absolute(
            participant.LINE_WIDTH.ACTUAL, participant.LINE_WIDTH.PERCEIVED, experiment
        )
        width_to_line = calculate_area.between_regression_and_reality_absolute(
            participant.WIDTH_LINE.ACTUAL, participant.WIDTH_LINE.PERCEIVED, experiment
        )

        width_to_width_areas.append(width_to_width)
        line_to_width_areas.append(line_to_width)
        width_to_line_areas.append(width_to_line)

    line_to_width_vs_width_to_line = [
        x - y for x, y in zip(line_to_width_areas, width_to_line_areas)
    ]
    line_to_width_vs_width_to_width = [
        x - y for x, y in zip(line_to_width_areas, width_to_width_areas)
    ]
    width_to_line_vs_width_to_width = [
        x - y for x, y in zip(width_to_line_areas, width_to_width_areas)
    ]

    lw_wl_mean, lw_wl_ci = utils.calculate_mean_ci(line_to_width_vs_width_to_line)
    lw_ww_mean, lw_ww_ci = utils.calculate_mean_ci(line_to_width_vs_width_to_width)
    wl_ww_mean, wl_ww_ci = utils.calculate_mean_ci(width_to_line_vs_width_to_width)

    utils.write_difference_mean_ci_header('exp1')
    utils.write_mean_ci_result(
        'exp1', lw_wl_mean, lw_wl_ci, "Grasp-to-vision", "Vision-to-grasp  -"
    )
    utils.write_mean_ci_result(
        'exp1', lw_ww_mean, lw_ww_ci, "Grasp-to-grasp", "Vision-to-grasp  -"
    )
    utils.write_mean_ci_result(
        'exp1', wl_ww_mean, wl_ww_ci, "Grasp-to-grasp", "Grasp-to-vision  -"
    )
    print(f"BETWEEN CONDITION DIFFERENCE - ERROR written.")
