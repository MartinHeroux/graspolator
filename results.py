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