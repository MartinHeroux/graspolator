import pandas as pd
import pingouin as pg
import numpy as np


import calculate_area
import utils


def write_icc_results(all_subject_data):
    r2_d1_dom = []
    r2_d2_dom = []
    area_d1_dom = []
    area_d2_dom = []

    for subject in all_subject_data:
        d1_dom_r2 = utils.calculate_r2(subject.day2_dominant_2.ACTUAL, subject.day2_dominant_2.PERCEIVED)
        d2_dom_r2 = utils.calculate_r2(subject.day2_dominant_1.ACTUAL, subject.day2_dominant_1.PERCEIVED)
        d1_dom_area = calculate_area.normalised(subject.day2_dominant_2.ACTUAL, subject.day2_dominant_2.PERCEIVED, 'exp1')
        d2_dom_area = calculate_area.normalised(subject.day2_dominant_1.ACTUAL, subject.day2_dominant_1.PERCEIVED, 'exp1')

        r2_d1_dom.append(d1_dom_r2)
        r2_d2_dom.append(d2_dom_r2)
        area_d1_dom.append(d1_dom_area)
        area_d2_dom.append(d2_dom_area)

    n_participants = len(all_subject_data)

    targets = _make_target_list(n_participants)
    test_session = _make_test_session_list(n_participants)

    high_r2 = r2_d1_dom + r2_d2_dom
    high_area = area_d1_dom + area_d2_dom

    high_r2_df = pd.DataFrame({'targets': targets, 'rater': test_session, 'score': high_r2})
    high_area_df = pd.DataFrame({'targets': targets, 'rater': test_session, 'score': high_area})

    high_r2_icc = pg.intraclass_corr(data=high_r2_df, targets='targets', raters='rater', ratings='score')
    high_area_icc = pg.intraclass_corr(data=high_area_df, targets='targets', raters='rater', ratings='score')


def _make_target_list(n_participants):
    targets = np.concatenate((np.arange(1, n_participants + 1, 1), np.arange(1, n_participants + 1, 1)), axis=0)
    targets = targets.tolist()

    return targets


def _make_test_session_list(n_participants):
    total_length = n_participants * 2
    test_session = []
    for i in range(total_length):
        if i < total_length/2:
            test_session.append('A')
        else:
            test_session.append('B')

    return test_session


def correlate_low_and_high_areas(all_subject_data):
    width_to_width_areas = []
    line_to_width_areas = []
    width_to_line_areas = []

    for participant in all_subject_data:
        width_to_width = calculate_area.normalised(participant.WIDTH_WIDTH.ACTUAL, participant.WIDTH_WIDTH.PERCEIVED, 'exp2')
        line_to_width = calculate_area.normalised(participant.LINE_WIDTH.ACTUAL, participant.LINE_WIDTH.PERCEIVED, 'exp2')
        width_to_line = calculate_area.normalised(participant.WIDTH_LINE.ACTUAL, participant.WIDTH_LINE.PERCEIVED, 'exp2')

        width_to_width_areas.append(width_to_width)
        line_to_width_areas.append(line_to_width)
        width_to_line_areas.append(width_to_line)

    if len(width_to_line_areas) + len(line_to_width_areas) + len(width_to_width_areas) != 90:
        print('Uneven lists')

    low_high_1 = utils.pearson_r_ci(width_to_width_areas, line_to_width_areas)
    low_high_2 = utils.pearson_r_ci(width_to_width_areas, width_to_line_areas)

    print(f'Width-width vs. Line-width r: {low_high_1[0]} 95%CI: {low_high_1[1]}')
    print(f'Width-width vs. Width-line r: {low_high_2[0]} 95%CI: {low_high_2[1]}')


def correlate_low_and_high_r2(all_subject_data):
    width_to_width_r2 = []
    line_to_width_r2 = []
    width_to_line_r2 = []

    for participant in all_subject_data:
        width_to_width = utils.calculate_r2(participant.WIDTH_WIDTH.ACTUAL, participant.WIDTH_WIDTH.PERCEIVED)
        line_to_width = utils.calculate_r2(participant.LINE_WIDTH.ACTUAL, participant.LINE_WIDTH.PERCEIVED)
        width_to_line = utils.calculate_r2(participant.WIDTH_LINE.ACTUAL, participant.WIDTH_LINE.PERCEIVED)

        width_to_width_r2.append(width_to_width)
        line_to_width_r2.append(line_to_width)
        width_to_line_r2.append(width_to_line)

    if len(width_to_line_r2) + len(line_to_width_r2) + len(width_to_width_r2) != 90:
        print('Uneven lists')

    low_high_1 = utils.pearson_r_ci(width_to_width_r2, line_to_width_r2)
    low_high_2 = utils.pearson_r_ci(width_to_width_r2, width_to_line_r2)

    print(f'Width-width vs. Line-width r: {low_high_1[0]} 95%CI: {low_high_1[1]}')
    print(f'Width-width vs. Width-line r: {low_high_2[0]} 95%CI: {low_high_2[1]}')