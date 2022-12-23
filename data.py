from typing import NamedTuple
from collections import namedtuple
from pathlib import Path
import numpy as np

import utils
from utils import get_directory_list, create_general_constants

general_constants = create_general_constants()


def return_all_subject_data(experiment, data_folder):
    """
    Return all participant data

    Parameters
    ----------
    experiment: str
        name of experiment
    data_folder: Pathlib.Path
        path to directory containing all subject data

    Returns
    -------
    list
        all subject data, one tuple per subject
    """
    if experiment == "exp1":
        all_subject_data = get_kathy_data(data_folder)

    elif experiment == "exp2":
        all_subject_data = return_lovisa_data(data_folder)

    else:
        SystemExit('Incorrect experiment string provided')

    if experiment == 'exp1':
        manuscript_experiment = 'exp2'
    else:
        manuscript_experiment = 'exp1'

    print(f'All subject data loaded for {manuscript_experiment}.')
    dashes = '-' * 60
    print(f'\n{dashes}\n')

    return all_subject_data


def return_all_subject_IDs(experiment, data_folder):
    """
        Return all participant identifiers

        Parameters
        ----------
        experiment: str
            name of experiment
        data_folder: Pathlib.Path
            path to directory containing all subject data

        Returns
        -------
        list
            participant IDs
        """
    if experiment == "exp1":
        subjects = get_directory_list(data_folder)

    elif experiment == "exp2":
        subjects = get_directory_list(data_folder)

    else:
        SystemExit('Incorrect experiment string provided')

    if experiment == 'exp1':
        manuscript_experiment = 'exp2'
    else:
        manuscript_experiment = 'exp1'

    print(f'All subject names loaded for {manuscript_experiment}.')
    dashes = '-' * 60
    print(f'\n{dashes}\n')

    return subjects

###########################################
# DEMOGRAPHICS
###########################################


def return_summary_demographics(experiment, data_folder):
    subjects = utils.get_directory_list(Path(f"./data/{experiment}"))

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


def return_participant_demographics(experiment, data_folder):
    subjects = utils.get_directory_list(Path(f"./data/{experiment}"))

    if experiment == "exp1":
        _remove_old_names(subjects)

    ages, sexes, handedness = [], [], []

    for subject in subjects:
        subject_folder = data_folder / subject
        demographic_txt = _read_dem_data(subject_folder)
        age, gender, hand = _extract_age_gender_handedness(
            experiment, demographic_txt
        )
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

        # widest_object_visual = demographic_txt[3].splilt(':')[1]
        # widest_object_grasp = demographic_txt[4].splilt(':')[1]

    if experiment == "exp2":
        age = demographic_txt[1].split(":")[1].strip()
        gender = demographic_txt[2].split(":")[1].strip()
        handedness = demographic_txt[3].split(":")[1].strip()

    return age, gender, handedness


############################################
# EXP1
############################################


def get_kathy_data(data_folder):
    all_subject_data = []
    subjects = general_constants.SUBJECT_IDS
    for subject in subjects:
        all_subject_data.append(_read_parse_exp1(data_folder, subject))
    return all_subject_data


def _read_parse_exp1(data_folder, subject):
    subject_folder = data_folder / subject
    current_subject_data = _read_subject_data(subject_folder)
    current_subject_data = _remove_ceiling_data_and_errors(current_subject_data, subject_folder, subject)
    blocks = _parse_data_to_block_tuples(current_subject_data)
    return blocks


def _remove_ceiling_data_and_errors(current_subject_data, subject_folder, subject):
    fix_file = subject_folder / (subject + "_fix.yaml")
    fix = utils.read_yaml_corrections_file(fix_file)
    if not fix_file.is_file():
        return current_subject_data
    if "delete" in fix:
        index = []
        deletion_target = fix["delete"]
        if deletion_target == 999:
            for i, line in enumerate(current_subject_data):
                if (line.split(":")[0].split("_")[0] == "MEASURE") and (
                    line.split(":")[1].strip() == "999"
                ):
                    index.append(i)
            index.reverse()
            #results = open("./results/results_exp1.txt", "a")
            print(
                f"{str(len(index)):5s} saturated data point(s) removed for {subject}\n"
            )
            #results.close()
            for index in index:
                current_subject_data.pop(index)
                current_subject_data.pop(index - 1)
            return current_subject_data
        else:
            current_subject_data.pop(deletion_target)
            current_subject_data.pop(deletion_target - 1)
            #results = open("./results/results_exp1.txt", "a")
            txt = "1"
            print(f"{txt:5s} outlier   data point(s) removed for {subject}\n")
            #results.close()
        return current_subject_data


def _read_subject_data(subject_folder):
    path_to_data_file = subject_folder / (subject_folder.name + "_data.txt")
    with open(path_to_data_file) as file:
        current_subject_data = file.readlines()
    return current_subject_data


def _parse_data_to_block_tuples(current_subject_data):
    actual_widths, perceived_widths, sides = _sequential_parsing(current_subject_data)
    actual_widths, perceived_widths = _remove_motor_error_trial(
        actual_widths, perceived_widths
    )
    actual_widths, perceived_widths = _reorder_based_on_hand_dominance(
        sides, actual_widths, perceived_widths
    )
    blocks = _extract_blocks(actual_widths, perceived_widths)
    return blocks


def _sequential_parsing(current_subject_data):
    count = -1
    actual_widths = [[], [], [], []]
    perceived_widths = [[], [], [], []]
    sides = []
    for line in current_subject_data:
        if line.split(":")[0] == "BLOCK":
            if line.split(":")[1].strip() == "WIDTH_TEST":
                break
            sides.append(line.split(":")[1].strip())
            count += 1
        if line.split(":")[0].split("_")[0] == "MEASURE":
            actual_width = int(line.split(":")[0].split("_")[2])
            perceived_width = float(line.split(":")[1].strip())
            actual_widths[count].append(actual_width)
            perceived_widths[count].append(perceived_width)
    return actual_widths, perceived_widths, sides


def _remove_motor_error_trial(actual_widths, perceived_widths):
    for i in range(4):
        actual_widths[i].pop(0)
        perceived_widths[i].pop(0)
    return actual_widths, perceived_widths


def _reorder_based_on_hand_dominance(sides, actual_widths, perceived_widths):
    if _dominant_not_first_on_day1(sides):
        actual_widths = _swap_order(actual_widths)
        perceived_widths = _swap_order(perceived_widths)
    return actual_widths, perceived_widths


def _dominant_not_first_on_day1(sides):
    return (
        (sides[3] == "LEFT")
        and (sides[0] == "RIGHT")
        or (sides[3] == "RIGHT")
        and (sides[0] == "LEFT")
    )


def _swap_order(list_of_lists):
    return [list_of_lists[1], list_of_lists[0], list_of_lists[2], list_of_lists[3]]


def _extract_blocks(actual_widths, perceived_widths):
    day1_dominant = Block_kathy(ACTUAL=actual_widths[0], PERCEIVED=perceived_widths[0])
    day1_non_dominant = Block_kathy(ACTUAL=actual_widths[1], PERCEIVED=perceived_widths[1])
    day2_dominant_1 = Block_kathy(ACTUAL=actual_widths[2], PERCEIVED=perceived_widths[2])
    day2_dominant_2 = Block_kathy(ACTUAL=actual_widths[3], PERCEIVED=perceived_widths[3])
    return Blocks_kathy(
        day1_dominant=day1_dominant,
        day1_non_dominant=day1_non_dominant,
        day2_dominant_1=day2_dominant_1,
        day2_dominant_2=day2_dominant_2,
    )


class Block_kathy(NamedTuple):
    ACTUAL: list
    PERCEIVED: list


class Blocks_kathy(NamedTuple):
    day1_dominant: Block_kathy
    day1_non_dominant: Block_kathy
    day2_dominant_1: Block_kathy
    day2_dominant_2: Block_kathy


############################################
# EXP2
############################################

def return_lovisa_data(data_folder):
    all_subject_blocked_data, subjects = _store_raw_blocked_data(data_folder)
    all_subject_data = []
    for subject_tuple, subject_ID in zip(all_subject_blocked_data, subjects):
        line_width_tuple = _parse_vision_to_grasp(
            subject_tuple.SHOW_LINE_PICK_WIDTH_BLOCK, subject_ID
        )
        width_width_tuple = _parse_grasp_to_vision(
            subject_tuple.PRESENT_WIDTH_PICK_WIDTH_BLOCK, subject_ID
        )
        width_line_tuple = _parse_grasp_to_grasp(
            subject_tuple.KATHY_EXPERIMENT_BLOCK, subject_ID
        )
        parsed_subject_data = Blocks_lovisa(
            SUBJECT_ID=subject_ID,
            LINE_WIDTH=line_width_tuple,
            WIDTH_WIDTH=width_width_tuple,
            WIDTH_LINE=width_line_tuple,
        )
        all_subject_data.append(parsed_subject_data)

    return all_subject_data


def _parse_vision_to_grasp(show_line_pick_width_block, subject_ID):
    actual_list = []
    perceived_list = []
    name = "line_width"
    for line in show_line_pick_width_block:
        if line.split("_")[0] == "SHOWLINE":
            actual_width_string = line.split(":")[0].split("_")[3]
            actual_width = (
                actual_width_string.replace("cm", "").replace("\n", "").replace(" ", "")
            )
            perceived_width = (
                (line.split(":")[1].split(" ")[1]).replace("\n", "").replace(" ", "")
            )
            actual_list.append(actual_width)
            perceived_list.append(perceived_width)
    actual_list, perceived_list = utils.remove_missing_data(
        actual_list, perceived_list, subject_ID, name
    )
    actuals = [float(i) for i in actual_list]
    perceived_widths = [float(i) for i in perceived_list]
    line_width_tuple = Block_lovisa(
        ACTUAL=actuals, PERCEIVED=perceived_widths, PLOT_INDEX=1
    )
    return line_width_tuple


def _parse_grasp_to_vision(present_width_pick_width_block, subject_ID):
    actual_list = []
    perceived_list = []
    name = "width_width"
    for line in present_width_pick_width_block:
        if line.split("_")[0] == "PRESENT":
            actual_width_string = line.split(":")[0].split("_")[4]
            actual_width = (
                actual_width_string.replace("cm", "").replace("\n", "").replace(" ", "")
            )
            perceived_width = (
                (line.split(":")[1].split(" ")[1]).replace("\n", "").replace(" ", "")
            )
            actual_list.append(actual_width)
            perceived_list.append(perceived_width)
    actual_list, perceived_list = utils.remove_missing_data(
        actual_list, perceived_list, subject_ID, name
    )
    actual_widths = [float(i) for i in actual_list]
    perceived_widths = [float(i) for i in perceived_list]
    width_width_tuple = Block_lovisa(
        ACTUAL=actual_widths, PERCEIVED=perceived_widths, PLOT_INDEX=3
    )
    return width_width_tuple


def _parse_grasp_to_grasp(kathy_experiment_block, subject_ID):
    actual_list = []
    perceived_list = []
    name = "kathy"
    for line in kathy_experiment_block:
        if "TRIAL" in line.split("-")[0]:
            actual_width = (
                line.split(":")[1].split(" ")[1].replace("\n", "").replace(" ", "")
            )
            actual_list.append(actual_width)
        if line.split("_")[0] == "MEASURE":
            perceived_width = (
                (line.split(":")[1].split(" ")[1]).replace("\n", "").replace(" ", "")
            )
            perceived_list.append(perceived_width)
    actual_list, perceived_list = utils.remove_missing_data(
        actual_list, perceived_list, subject_ID, name
    )
    actual_widths = [float(i) for i in actual_list]
    perceived_widths = [float(i) for i in perceived_list]
    width_line_tuple = Block_lovisa(
        ACTUAL=actual_widths, PERCEIVED=perceived_widths, PLOT_INDEX=2
    )
    return width_line_tuple


def _store_raw_blocked_data(data_folder):
    all_subject_blocked_data = []
    subjects = utils.get_directory_list(Path("./data/exp2"))
    for subject in subjects:
        all_subject_blocked_data.append(_read_block_exp2(data_folder, subject))
    return all_subject_blocked_data, subjects


def _read_block_exp2(data_folder, subject):
    subject_folder = data_folder / subject
    current_subject_data = _read_subject_data(subject_folder)
    block_start_indices, block_order_names = _store_block_names_and_indices(
        current_subject_data
    )
    unordered_blocked_data = _unnamed_blocked_raw_data(
        current_subject_data, block_start_indices, block_order_names
    )
    named_block_data = _named_blocked_raw_data(
        unordered_blocked_data, block_order_names
    )
    return named_block_data


def _store_block_names_and_indices(current_subject_data):
    block_start_indices = []
    block_order_names = []
    for line_number, line in enumerate(current_subject_data, start=0):
        if line.split(":")[0] == "BLOCK":
            block_start_indices.append(line_number)
            block_name = str(line.split(":")[1]).strip()
            block_name = block_name.replace(" ", "_")
            block_order_names.append(block_name)
    return block_start_indices, block_order_names


def _unnamed_blocked_raw_data(
    current_subject_data, block_start_indices, block_order_names
):
    block_start_indices.reverse()
    block_order_names.reverse()
    blocked_data_lists = []

    for block_start_index in block_start_indices:
        block_data = current_subject_data[block_start_index:]
        block_data.pop(0)
        current_subject_data = current_subject_data[0:block_start_index]
        blocked_data_lists.append(block_data)

    return blocked_data_lists


def _named_blocked_raw_data(unordered_blocked_data, block_order_names):
    block_order_names.reverse
    " ".join(block_order_names)
    subject_data = namedtuple("SUBJECT", block_order_names)
    subject_tuple = subject_data._make(unordered_blocked_data)
    return subject_tuple


class Block_lovisa(NamedTuple):
    ACTUAL: object
    PERCEIVED: object
    PLOT_INDEX: object


class Blocks_lovisa(NamedTuple):
    SUBJECT_ID: object
    WIDTH_WIDTH: Block_lovisa
    LINE_WIDTH: Block_lovisa
    WIDTH_LINE: Block_lovisa



