from typing import NamedTuple

import utils

general_constants = utils.create_general_constants()

def read_exp1(data_folder):
    blocked_data = []
    widest_lines = []
    subjects = general_constants.SUBJECT_IDS
    for subject in subjects:
        blocked_data.append(_read_parse_exp1(data_folder, subject)[0])
        widest_lines.append(_read_parse_exp1(data_folder, subject)[1])
    return blocked_data, widest_lines


def _read_parse_exp1(data_folder, subject):
    subject_folder = data_folder / subject
    current_subject_data = _read_subject_data(subject_folder)
    current_subject_data = _fix_data(current_subject_data, subject_folder, subject)
    widest_line = _extract_widest_line_based_on_visual_inspection(
        current_subject_data
    )
    blocks = _parse_data(current_subject_data)
    return blocks, widest_line


def _fix_data(current_subject_data, subject_folder, subject):
    fix_file = subject_folder / (subject + '_fix.yaml')
    fix = utils.read_yaml_corrections_file(fix_file)
    if not fix_file.is_file():
        return current_subject_data
    if 'delete' in fix:
        index = []
        deletion_target = fix['delete']
        if deletion_target == 999:
            for i, line in enumerate(current_subject_data):
                if (line.split(":")[0].split("_")[0] == "MEASURE") and (line.split(":")[1].strip() == '999'):
                    index.append(i)
            index.reverse()
            for index in index:
                current_subject_data.pop(index)
                current_subject_data.pop(index-1)
            return current_subject_data
        else:
            current_subject_data.pop(deletion_target)
            current_subject_data.pop(deletion_target - 1)
        return current_subject_data

def _read_subject_data(subject_folder):
    path_to_data_file = subject_folder / (subject_folder.name + "_data.txt")
    with open(path_to_data_file) as file:
        current_subject_data = file.readlines()
    return current_subject_data


def _extract_widest_line_based_on_visual_inspection(current_subject_data):
    widest_line = current_subject_data.pop(-1).split(":")[1].strip()
    return widest_line  # , current_subject_data


def _parse_data(current_subject_data):
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
    day1_dominant = Block(
        actual_widths=actual_widths[0], perceived_widths=perceived_widths[0]
    )
    day1_non_dominant = Block(
        actual_widths=actual_widths[1], perceived_widths=perceived_widths[1]
    )
    day2_dominant_1 = Block(
        actual_widths=actual_widths[2], perceived_widths=perceived_widths[2]
    )
    day2_dominant_2 = Block(
        actual_widths=actual_widths[3], perceived_widths=perceived_widths[3]
    )
    return Blocks(
        day1_dominant=day1_dominant,
        day1_non_dominant=day1_non_dominant,
        day2_dominant_1=day2_dominant_1,
        day2_dominant_2=day2_dominant_2,
    )


class Block(NamedTuple):
    actual_widths: list
    perceived_widths: list


class Blocks(NamedTuple):
    day1_dominant: Block
    day1_non_dominant: Block
    day2_dominant_1: Block
    day2_dominant_2: Block
