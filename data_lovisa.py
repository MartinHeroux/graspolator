from dataclasses import dataclass

import data_utils
import utils


def get_lovisa_data(data_folder):
    study_raw_data, subjects = _get_raw_blocked_data(data_folder)
    study_data = []
    for subject_data, subject in zip(study_raw_data, subjects):
        line_width = _parse_vision_to_grasp(
            subject_data.SHOW_LINE_PICK_WIDTH_BLOCK, subject
        )
        width_width = _parse_grasp_to_vision(
            subject_data.PRESENT_WIDTH_PICK_WIDTH_BLOCK, subject
        )
        width_line = _parse_grasp_to_grasp(subject_data.KATHY_EXPERIMENT_BLOCK, subject)
        parsed_subject_data = BlocksLovisa(
            subject_id=subject,
            line_width=line_width,
            width_width=width_width,
            width_line=width_line,
        )
        study_data.append(parsed_subject_data)
    return study_data


def _parse_vision_to_grasp(show_line_pick_width_block, subject):
    actual_list = list()
    perceived_list = list()
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

    actual_list, perceived_list = data_utils.remove_missing_data(
        actual_list, perceived_list, subject
    )

    actual = [float(i) for i in actual_list]
    perceived = [float(i) for i in perceived_list]

    line_width = data_utils.GraspolatorBlock(
        actual=actual, perceived=perceived, plot_index=1
    )
    line_width.compute_outcomes()

    return line_width


def _parse_grasp_to_vision(present_width_pick_width_block, subject):
    actual_list = []
    perceived_list = []
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

    actual_list, perceived_list = data_utils.remove_missing_data(
        actual_list, perceived_list, subject
    )
    actual_widths = [float(i) for i in actual_list]
    perceived_widths = [float(i) for i in perceived_list]
    width_width = data_utils.GraspolatorBlock(
        actual=actual_widths, perceived=perceived_widths, plot_index=3
    )
    width_width.compute_outcomes()

    return width_width


def _parse_grasp_to_grasp(kathy_experiment_block, subject):
    actual_list = list()
    perceived_list = list()
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

    actual_list, perceived_list = data_utils.remove_missing_data(
        actual_list, perceived_list, subject
    )
    actual_widths = [float(i) for i in actual_list]
    perceived_widths = [float(i) for i in perceived_list]
    width_line = data_utils.GraspolatorBlock(
        actual=actual_widths, perceived=perceived_widths, plot_index=2
    )
    width_line.compute_outcomes()
    return width_line


def _get_raw_blocked_data(data_folder):
    all_subject_blocked_data = []
    subjects = utils.get_subject_ids(data_folder)
    for subject in subjects:
        all_subject_blocked_data.append(_read_block_exp2(data_folder, subject))
    return all_subject_blocked_data, subjects


def _read_block_exp2(data_folder, subject):
    subject_folder = data_folder / subject
    current_subject_data = data_utils.read_subject_data(subject_folder)
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
    for block_name, block_raw_data in zip(block_order_names, unordered_blocked_data):
        if block_name == "KATHY_EXPERIMENT_BLOCK":
            KATHY_EXPERIMENT_BLOCK = block_raw_data
        if block_name == "PRESENT_WIDTH_PICK_WIDTH_BLOCK":
            PRESENT_WIDTH_PICK_WIDTH_BLOCK = block_raw_data
        if block_name == "SHOW_LINE_PICK_WIDTH_BLOCK":
            SHOW_LINE_PICK_WIDTH_BLOCK = block_raw_data

    return RawBlockLovisa(
        KATHY_EXPERIMENT_BLOCK=KATHY_EXPERIMENT_BLOCK,
        PRESENT_WIDTH_PICK_WIDTH_BLOCK=PRESENT_WIDTH_PICK_WIDTH_BLOCK,
        SHOW_LINE_PICK_WIDTH_BLOCK=SHOW_LINE_PICK_WIDTH_BLOCK,
    )


@dataclass
class RawBlockLovisa:
    KATHY_EXPERIMENT_BLOCK: list
    PRESENT_WIDTH_PICK_WIDTH_BLOCK: list
    SHOW_LINE_PICK_WIDTH_BLOCK: list


@dataclass
class BlocksLovisa:
    subject_id: str
    width_width: data_utils.GraspolatorBlock
    line_width: data_utils.GraspolatorBlock
    width_line: data_utils.GraspolatorBlock
