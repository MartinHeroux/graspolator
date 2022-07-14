import pandas as pd
import pingouin as pg
import numpy as np


import calculate_area
import utils


def write_intercept_slope_summary(all_subject_data, experiment):
    if experiment == 'exp1':
        intercept_lists = [[], [], [], []]
        slope_lists = [[], [], [], []]
        condition_names = ['day 1 dominant', 'day 1 non-dominant', 'day 2 dominant 1', 'day 2 dominant 2']
    else:
        intercept_lists = [[], [], []]
        slope_lists = [[], [], []]
        condition_names = ['line to width', 'width to line', 'width to width']

    for subject_data in all_subject_data:
        data_list = utils.create_data_tuples(experiment, subject_data)
        for condition_data, label, condition_name, intercept_list, slope_list in zip(data_list, condition_names, intercept_lists, slope_lists):
            intercept, slope = utils.calculate_regression_general(condition_data.ACTUAL, condition_data.PERCEIVED)
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

    results = open(f'results_{experiment}.txt', 'a')
    results.write('\n')
    results.close()

    for condition_name, intercept_mean, intercept_ci, slope_mean, slope_ci in zip(condition_names, intercept_means, intercept_cis, slope_means, slope_cis):
        utils.write_mean_ci_result(experiment, intercept_mean, intercept_ci, 'intercept', condition_name)
        utils.write_mean_ci_result(experiment, slope_mean, slope_ci, 'slope', condition_name)

    print(f'Intercept and slope summary results written to results_{experiment}.txt')


def write_icc_results(all_subject_data):
    r2_d1_dom = []
    r2_d2_dom = []
    area_d1_dom = []
    area_d2_dom = []

    for subject in all_subject_data:
        d1_dom_r2 = utils.calculate_r2(subject.day1_dominant.ACTUAL, subject.day1_dominant.PERCEIVED)
        d2_dom_r2 = utils.calculate_r2(subject.day2_dominant_1.ACTUAL, subject.day2_dominant_1.PERCEIVED)
        d1_dom_area = calculate_area.normalised(subject.day1_dominant.ACTUAL, subject.day1_dominant.PERCEIVED, 'exp1')
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


def between_condition_r2_mean_difference(all_subject_data):
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

    line_to_width_vs_width_to_line = [abs(x - y) for x, y in zip(line_to_width_r2, width_to_line_r2)]
    line_to_width_vs_width_to_width = [abs(x - y) for x, y in zip(line_to_width_r2, width_to_width_r2)]
    width_to_line_vs_width_to_width = [abs(x - y) for x, y in zip(width_to_line_r2, width_to_width_r2)]

    lw_wl_mean, lw_wl_ci = utils.calculate_mean_ci(line_to_width_vs_width_to_line)
    lw_ww_mean, lw_ww_ci = utils.calculate_mean_ci(line_to_width_vs_width_to_width)
    wl_ww_mean, wl_ww_ci = utils.calculate_mean_ci(width_to_line_vs_width_to_width)

    print(f'Line-to-width vs width-to-line R2\nMean difference: {lw_wl_mean:4.2f}[{lw_wl_mean - lw_wl_ci:4.2f} to {lw_wl_mean + lw_wl_ci:4.2f}]\n\n')
    print(f'Line to width vs width_to_width R2\nMean difference: {lw_ww_mean:4.2f}[{lw_ww_mean - lw_ww_ci:4.2f} to {lw_ww_mean + lw_ww_ci:4.2f}]\n')
    print(f'Width to line vs width-to-width R2\nMean difference: {wl_ww_mean:4.2f}[{wl_ww_mean - wl_ww_ci:4.2f} to {wl_ww_mean + wl_ww_ci:4.2f}]\n')


def between_condition_area_mean_difference(all_subject_data):
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

    line_to_width_vs_width_to_line = [abs(x - y) for x, y in zip(line_to_width_areas, width_to_line_areas)]
    line_to_width_vs_width_to_width = [abs(x - y) for x, y in zip(line_to_width_areas, width_to_width_areas)]
    width_to_line_vs_width_to_width = [abs(x - y) for x, y in zip(width_to_line_areas, width_to_width_areas)]

    lw_wl_mean, lw_wl_ci = utils.calculate_mean_ci(line_to_width_vs_width_to_line)
    lw_ww_mean, lw_ww_ci = utils.calculate_mean_ci(line_to_width_vs_width_to_width)
    wl_ww_mean, wl_ww_ci = utils.calculate_mean_ci(width_to_line_vs_width_to_width)

    print(
        f'Line-to-width vs width-to-line Area\nMean difference: {lw_wl_mean:4.2f}[{lw_wl_mean - lw_wl_ci:4.2f} to {lw_wl_mean + lw_wl_ci:4.2f}]\n\n')
    print(
        f'Line to width vs width_to_width Area\nMean difference: {lw_ww_mean:4.2f}[{lw_ww_mean - lw_ww_ci:4.2f} to {lw_ww_mean + lw_ww_ci:4.2f}]\n')
    print(
        f'Width to line vs width-to-width Area\nMean difference: {wl_ww_mean:4.2f}[{wl_ww_mean - wl_ww_ci:4.2f} to {wl_ww_mean + wl_ww_ci:4.2f}]\n')