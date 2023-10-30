from pathlib import Path
import os

import numpy as np
from scipy import stats

import utils

RESULTS_PATH = utils.create_results_save_path()


def write_participant_demographics(results_txt, experiment, data_folder):
    write_result_header(results_txt, "Subject demographics")
    age_mean, age_sd, number_females, right_handed = _return_summary_demographics(
        experiment, data_folder
    )

    results = open(results_txt, "a")
    age = "Age mean:"
    fem = "N females:"
    right = "R handed:"
    results.write(
        f"{age:10s} {age_mean:3.1f} (SD: {age_sd:3.1f})\n{fem:10s} {number_females:10s}\n{right:10s} {right_handed:5s}\n\n"
    )
    results.close()


def _return_summary_demographics(experiment, data_folder):
    subjects = utils.get_subject_ids(Path(f"./data/{experiment}"))

    if experiment == "exp1":
        _remove_old_names(subjects)

    ages, genders, handednessi = [], [], []

    for subject in subjects:
        subject_folder = data_folder / subject
        demographic_txt = _read_dem_data(subject_folder)
        age, gender, handedness = _extract_age_gender_handedness(
            experiment, demographic_txt
        )
        ages.append(int(age))
        genders.append(gender)
        handednessi.append(handedness)

    age_mean, age_sd = np.mean(ages), np.std(ages)
    if experiment == "exp1":
        number_females = genders.count("F")
        right_handed = handednessi.count("R")
    else:
        number_females = genders.count("f")
        right_handed = handednessi.count("r")

    return age_mean, age_sd, str(number_females), str(right_handed)


def _return_participant_demographics(experiment, data_folder):
    subjects = utils.get_subject_ids(Path(f"./data/{experiment}"))

    if experiment == "exp1":
        _remove_old_names(subjects)

    ages, sexes, handedness = [], [], []

    for subject in subjects:
        subject_folder = data_folder / subject
        demographic_txt = _read_dem_data(subject_folder)
        age, gender, hand = _extract_age_gender_handedness(experiment, demographic_txt)
        ages.append(int(age))
        sexes.append(gender)
        handedness.append(hand)

    return ages, sexes, handedness


def _read_dem_data(subject_folder):
    path_to_data_file = subject_folder / (subject_folder.name + ".txt")
    with open(path_to_data_file) as file:
        current_subject_data = file.readlines()
    return current_subject_data


def _remove_old_names(subjects):
    if len(subjects) == 32:
        subjects.pop(-1)
        subjects.pop(-1)

    if len(subjects) != 30:
        print("Error in popping 'old' directories")
        exit
    else:
        print(f"Subject names successfully edited {len(subjects)}")


def _extract_age_gender_handedness(experiment, demographic_txt):
    if experiment == "exp1":
        age = demographic_txt[0].split(":")[1].strip()
        gender = demographic_txt[1].split(":")[1].strip()
        handedness = demographic_txt[2].split(":")[1].strip()

    if experiment == "exp2":
        age = demographic_txt[1].split(":")[1].strip()
        gender = demographic_txt[2].split(":")[1].strip()
        handedness = demographic_txt[3].split(":")[1].strip()

    return age, gender, handedness


def gen_results_txt(study):
    results_txt = Path(RESULTS_PATH, f"results_{study}.txt")
    if results_txt.exists():
        os.remove(results_txt)
        print(f"Previous results_{study}.txt removed\n")
    print(f"Starting to write to {results_txt}.\n")
    return results_txt


def calculate_mean_ci(data_list):
    mean = np.mean(data_list)
    confidence = 0.95
    n = len(data_list)
    std_err = stats.sem(data_list)
    moe = std_err * stats.t.ppf((1 + confidence) / 2, n - 1)
    ci = (mean - moe, mean + moe)
    return mean, ci


def write_result_header(results_txt, result_name):
    with open(results_txt, "a") as f:
        f.write("\n\n")
        f.write("-" * 80)
        f.write("\n")
        f.write(f"{result_name}")
        f.write("\n")
        f.write("-" * 80)
        f.write("\n")


def write_results_outcome_header(results_txt):
    with open(results_txt, "a") as f:
        f.write("\n")
        f.write(f"{'': <20s} {'mean': <8s} {'95%CI': <10s}")


def write_results(results_txt, block_name, mean, ci):
    with open(results_txt, "a") as f:
        f.write("\n")
        f.write(f"{block_name:<20s} {mean: >6.2f} [{ci[0]: <3.2f} to {ci[1]: <3.2f}]")


def write_subject_outcome_header(results_txt):
    with open(results_txt, "a") as f:
        f.write(
            f"{'subject': <8s} {'inter': >6s} {'slope': >6s} {'r-sq': >6s} {'MAE': >6s}"
        )


def write_all_subject_results_lovisa(results_txt, all_subject_data):
    write_result_header(results_txt, "Subject Results")
    with open(results_txt, "a") as f:
        f.write("\n")
        f.write("vision-to-grasp")
        f.write("\n")

    write_subject_outcome_header(results_txt)
    with open(results_txt, "a") as f:
        for subject in all_subject_data:
            f.write("\n")
            f.write(
                f"{subject.subject_id: <8s} {subject.line_width.intercept: >6.2f} {subject.line_width.slope: >6.2f} "
                f"{subject.line_width.r_squared: >6.2f} {subject.line_width.mean_abs_error: >6.2f}"
            )

    with open(results_txt, "a") as f:
        f.write("\n\n")
        f.write("grasp_to_vision")
        f.write("\n")

    write_subject_outcome_header(results_txt)

    with open(results_txt, "a") as f:
        for subject in all_subject_data:
            f.write("\n")
            f.write(
                f"{subject.subject_id: <8s} {subject.width_line.intercept: >6.2f} {subject.width_line.slope: >6.2f} "
                f"{subject.width_line.r_squared: >6.2f} {subject.width_line.mean_abs_error: >6.2f}"
            )

    with open(results_txt, "a") as f:
        f.write("\n\n")
        f.write("grasp_to_grasp")
        f.write("\n")
    write_subject_outcome_header(results_txt)
    with open(results_txt, "a") as f:
        for subject in all_subject_data:
            f.write("\n")
            f.write(
                f"{subject.subject_id: <8s} {subject.width_width.intercept: >6.2f} {subject.width_width.slope: >6.2f} "
                f"{subject.width_width.r_squared: >6.2f} {subject.width_width.mean_abs_error: >6.2f}"
            )


def write_all_subject_results_kathy(results_txt, study_data):
    write_result_header(results_txt, "Subject Results")

    with open(results_txt, "a") as f:
        f.write("\n")
        f.write("day1_dominant")
        f.write("\n")
    write_subject_outcome_header(results_txt)
    with open(results_txt, "a") as f:
        for subject in study_data:
            f.write("\n")
            f.write(
                f"{subject.subject: <8s} {subject.day1_dominant.intercept: >6.2f} {subject.day1_dominant.slope: >6.2f} "
                f"{subject.day1_dominant.r_squared: >6.2f} {subject.day1_dominant.mean_abs_error: >6.2f}"
            )

    with open(results_txt, "a") as f:
        f.write("\n\n")
        f.write("day1_non_dominant")
        f.write("\n")
    write_subject_outcome_header(results_txt)
    with open(results_txt, "a") as f:
        for subject in study_data:
            f.write("\n")
            f.write(
                f"{subject.subject: <8s} {subject.day1_non_dominant.intercept: >6.2f} {subject.day1_non_dominant.slope: >6.2f} "
                f"{subject.day1_non_dominant.r_squared: >6.2f} {subject.day1_non_dominant.mean_abs_error: >6.2f}"
            )
    with open(results_txt, "a") as f:
        f.write("\n\n")
        f.write("day2_dominant_1")
        f.write("\n")
    write_subject_outcome_header(results_txt)
    with open(results_txt, "a") as f:
        for subject in study_data:
            f.write("\n")
            f.write(
                f"{subject.subject: <8s} {subject.day2_dominant_1.intercept: >6.2f} {subject.day2_dominant_1.slope: >6.2f} "
                f"{subject.day2_dominant_1.r_squared: >6.2f} {subject.day2_dominant_1.mean_abs_error: >6.2f}"
            )

    with open(results_txt, "a") as f:
        f.write("\n\n")
        f.write("day2_dominant_2")
        f.write("\n")
    write_subject_outcome_header(results_txt)
    with open(results_txt, "a") as f:
        for subject in study_data:
            f.write("\n")
            f.write(
                f"{subject.subject: <8s} {subject.day2_dominant_2.intercept: >6.2f} {subject.day2_dominant_2.slope: >6.2f} "
                f"{subject.day2_dominant_2.r_squared: >6.2f} {subject.day2_dominant_2.mean_abs_error: >6.2f}"
            )


def calc_diff_two_lines_relative_unity(
    inter1, slope1, inter2, slope2, min_width, max_width
):
    errors = list()
    true_errors = list()
    for width in range(int(min_width), int(max_width) + 1):
        value_1 = (slope1 * width) + inter1
        value_2 = (slope2 * width) + inter2
        error = abs(value_1 - value_2)

        if value_2 > width:
            new_value_2 = width - (value_2 - width)
        else:
            new_value_2 = width + (width - value_2)

        true_error = abs(value_1 - new_value_2)
        errors.append(error)
        true_errors.append(true_error)

    return np.mean(errors), np.mean(true_errors)


def calc_diff_two_lines_(inter1, slope1, inter2, slope2, min_width, max_width):
    errors = list()
    for width in range(int(min_width), int(max_width) + 1):
        value_1 = (slope1 * width) + inter1
        value_2 = (slope2 * width) + inter2
        error = abs(value_1 - value_2)
        errors.append(error)
    return np.mean(errors)
