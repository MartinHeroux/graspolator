import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from pathlib import Path
from random import random
import random as rd
import os
from collections import namedtuple
from matplotlib.lines import Line2D

import utils
import area_calcs

def plot_regression_widest_perceived(subject_IDs, all_subject_data):
    condition_names = ['day1_dominant', "day1_non_dominant", "day2_dominant_1", "day2_dominant_2"]
    subplot_indices = [1, 2, 3, 4]

    plt.figure(figsize=(15, 5))
    plt.suptitle(str('Participant Regression Lines'))

def data_cleaning(subject_IDs, all_subject_data):
    subjects_with_10_removed = []

    d1_dom_at_10, d1_non_dom_at_10, d2_dom_1_at_10, d2_dom_2_at_10 = [], [], [], []

    for subject_ID, current_subject_data in zip(subject_IDs, all_subject_data):
        d1_dom, d1_non_dom, d2_dom_1, d2_dom_2 = perceived_at_10(current_subject_data)

        d1_dom_at_10.append(d1_dom)
        d1_non_dom_at_10.append(d1_non_dom)
        d2_dom_1_at_10.append(d2_dom_1)
        d2_dom_2_at_10.append(d2_dom_2)


def perceived_at_10(subject_ID, current_subject_data):

    d1_dom = average_at_10(subject_ID, current_subject_data[0])
    d1_non_dom = average_at_10(subject_ID, current_subject_data[1])
    d2_dom_1 = average_at_10(subject_ID, current_subject_data[2])
    d2_dom_2 = average_at_10(subject_ID, current_subject_data[3])

    return d1_dom, d1_non_dom, d2_dom_1, d2_dom_2


def average_at_10(subject_ID, block):
    actual_widths = block.actual_widths
    perceived_widths = block.perceived_widths

    perceived_at_10 = []

    for actual_width, perceived_width in zip(actual_widths, perceived_widths):
        if actual_width == 10:
            perceived_at_10.append(perceived_width)

    if 10 not in actual_widths:
        subjects_with_10_removed.append(subject_ID)

    average_at_10 = np.mean(perceived_at_10)

    return average_at_10



