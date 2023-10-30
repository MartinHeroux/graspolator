from dataclasses import dataclass

import data_utils
import utils


def get_kathy_data(data_folder):
    return _get_raw_blocked_data(data_folder)


def _get_raw_blocked_data(data_folder):
    all_subject_blocked_data = []
    subjects = utils.get_subject_ids(data_folder)
    for subject in subjects:
        all_subject_blocked_data.append(_read_block_exp1(data_folder, subject))
    return all_subject_blocked_data


def _read_block_exp1(data_folder, subject):
    subject_folder = data_folder / subject
    current_subject_data = data_utils.read_subject_data(subject_folder)
    current_subject_data = _remove_ceiling_data_and_errors(
        current_subject_data, subject_folder, subject
    )
    blocks = _parse_data_to_block_tuples(current_subject_data)
    blocks.subject = subject
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
            print(
                f"{str(len(index)):5s} saturated data point(s) removed for {subject}\n"
            )
            for index in index:
                current_subject_data.pop(index)
                current_subject_data.pop(index - 1)
            return current_subject_data
        else:
            current_subject_data.pop(deletion_target)
            current_subject_data.pop(deletion_target - 1)
            txt = "1"
            print(f"{txt:5s} outlier   data point(s) removed for {subject}\n")
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
    day1_dominant = data_utils.GraspolatorBlock(
        actual=actual_widths[0], perceived=perceived_widths[0], plot_index=1
    )
    day1_dominant.compute_outcomes()
    day1_non_dominant = data_utils.GraspolatorBlock(
        actual=actual_widths[1], perceived=perceived_widths[1], plot_index=2
    )
    day1_non_dominant.compute_outcomes()
    day2_dominant_1 = data_utils.GraspolatorBlock(
        actual=actual_widths[2], perceived=perceived_widths[2], plot_index=3
    )
    day2_dominant_1.compute_outcomes()
    day2_dominant_2 = data_utils.GraspolatorBlock(
        actual=actual_widths[3], perceived=perceived_widths[3], plot_index=4
    )
    day2_dominant_2.compute_outcomes()
    return BlocksKathy(
        day1_dominant=day1_dominant,
        day1_non_dominant=day1_non_dominant,
        day2_dominant_1=day2_dominant_1,
        day2_dominant_2=day2_dominant_2,
    )


@dataclass
class BlocksKathy:
    day1_dominant: data_utils.GraspolatorBlock
    day1_non_dominant: data_utils.GraspolatorBlock
    day2_dominant_1: data_utils.GraspolatorBlock
    day2_dominant_2: data_utils.GraspolatorBlock
    subject: str = ""
