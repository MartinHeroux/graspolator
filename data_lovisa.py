from collections import namedtuple
from typing import NamedTuple
from pathlib import Path

import utils_lovisa


def process_blocked_data():
    data_folder = Path('./data/exp2')
    all_subject_blocked_data, subjects = _store_raw_blocked_data(data_folder)
    parsed_group_data = []
    for subject_tuple, subject_ID in zip(all_subject_blocked_data, subjects):
        line_width_tuple = _parse_show_line_pick_width(subject_tuple.SHOW_LINE_PICK_WIDTH_BLOCK, subject_ID)
        width_width_tuple = _parse_present_width_pick_width(subject_tuple.PRESENT_WIDTH_PICK_WIDTH_BLOCK, subject_ID)
        width_line_tuple = _parse_kathy_block(subject_tuple.KATHY_EXPERIMENT_BLOCK, subject_ID)
        parsed_subject_data = Blocks(SUBJECT_ID=subject_ID,
                                     LINE_WIDTH=line_width_tuple,
                                     WIDTH_WIDTH=width_width_tuple,
                                     WIDTH_LINE=width_line_tuple)
        parsed_group_data.append(parsed_subject_data)

    return parsed_group_data


def _parse_show_line_pick_width(show_line_pick_width_block, subject_ID):
    actual_list = []
    perceived_list= []
    name = 'line_width'
    for line in show_line_pick_width_block:
        if line.split("_")[0] == "SHOWLINE":
            actual_width_string = (line.split(":")[0].split("_")[3])
            actual_width = actual_width_string.replace('cm', '').replace("\n", "").replace(" ", "")
            perceived_width = (line.split(":")[1].split(" ")[1]).replace("\n", "").replace(" ", "")
            actual_list.append(actual_width)
            perceived_list.append(perceived_width)
    actual_list, perceived_list = utils_lovisa.remove_missing_data(actual_list, perceived_list, subject_ID, name)
    actuals = [float(i) for i in actual_list]
    perceived_widths = [float(i) for i in perceived_list]
    line_width_tuple = Block(ACTUAL=actuals, PERCEIVED=perceived_widths, PLOT_INDEX=1)
    return line_width_tuple


def _parse_present_width_pick_width(present_width_pick_width_block, subject_ID):
    actual_list = []
    perceived_list = []
    name = 'width_width'
    for line in present_width_pick_width_block:
        if line.split("_")[0] == "PRESENT":
            actual_width_string = (line.split(":")[0].split("_")[4])
            actual_width = actual_width_string.replace('cm', '').replace("\n", "").replace(" ", "")
            perceived_width = (line.split(":")[1].split(" ")[1]).replace("\n", "").replace(" ", "")
            actual_list.append(actual_width)
            perceived_list.append(perceived_width)
    actual_list, perceived_list = utils_lovisa.remove_missing_data(actual_list, perceived_list, subject_ID, name)
    actual_widths = [float(i) for i in actual_list]
    perceived_widths = [float(i) for i in perceived_list]
    width_width_tuple = Block(ACTUAL=actual_widths, PERCEIVED=perceived_widths, PLOT_INDEX=3)
    return width_width_tuple


def _parse_kathy_block(kathy_experiment_block, subject_ID):
    actual_list = []
    perceived_list = []
    name = 'kathy'
    for line in kathy_experiment_block:
        if "TRIAL" in line.split("-")[0]:
            actual_width = line.split(':')[1].split(' ')[1].replace("\n", "").replace(" ", "")
            actual_list.append(actual_width)
        if line.split("_")[0] == "MEASURE":
            perceived_width = (line.split(":")[1].split(" ")[1]).replace("\n", "").replace(" ", "")
            perceived_list.append(perceived_width)
    actual_list, perceived_list = utils_lovisa.remove_missing_data(actual_list, perceived_list, subject_ID, name)
    actual_widths = [float(i) for i in actual_list]
    perceived_widths = [float(i) for i in perceived_list]
    width_line_tuple = Block(ACTUAL=actual_widths, PERCEIVED=perceived_widths, PLOT_INDEX=2)
    return width_line_tuple


def _store_raw_blocked_data(data_folder):
    all_subject_blocked_data = []
    subjects = utils_lovisa.get_directory_list(Path('./data/exp2'))
    for subject in subjects:
        all_subject_blocked_data.append(_read_block_exp1(data_folder, subject))
    return all_subject_blocked_data, subjects


def _read_block_exp1(data_folder, subject):
    subject_folder = data_folder / subject
    current_subject_data = _read_subject_data(subject_folder)
    block_start_indices, block_order_names = _store_block_names_and_indices(current_subject_data)
    unordered_blocked_data = _unnamed_blocked_raw_data(current_subject_data, block_start_indices, block_order_names)
    named_block_data = _named_blocked_raw_data(unordered_blocked_data, block_order_names)
    return named_block_data


def _read_subject_data(subject_folder):
    path_to_data_file = subject_folder / (subject_folder.name + "_data.txt")
    with open(path_to_data_file) as file:
        current_subject_data = file.readlines()
    return current_subject_data


def _store_block_names_and_indices(current_subject_data):
    block_start_indices = []
    block_order_names = []
    for line_number, line in enumerate(current_subject_data, start=0):
        if line.split(":")[0] == "BLOCK":
            block_start_indices.append(line_number)
            block_name = str(line.split(':')[1]).strip()
            block_name = block_name.replace(" ", "_")
            block_order_names.append(block_name)
    return block_start_indices, block_order_names


def _unnamed_blocked_raw_data(current_subject_data, block_start_indices, block_order_names):
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
    ' '.join(block_order_names)
    subject_data = namedtuple('SUBJECT', block_order_names)
    subject_tuple = subject_data._make(unordered_blocked_data)
    return subject_tuple


class Block(NamedTuple):
    ACTUAL: object
    PERCEIVED: object
    PLOT_INDEX: object


class Blocks(NamedTuple):
    SUBJECT_ID: object
    WIDTH_WIDTH: Block
    LINE_WIDTH: Block
    WIDTH_LINE: Block
