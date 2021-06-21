from collections import namedtuple

import plot_journal
import process
import plot


plot_dispatch = namedtuple('plot_dispatch', 'PLOT COMMAND')


# TODO change string below to match experiment
#  either 'exp1' or 'exp2' (Kathy and Lovisa respectively)
#experiments = ['exp1', 'exp2']
experiments = ['exp1', 'exp2']
experiment = 'exp2'
for experiment in experiments:
    # import data and subject list for experiment
    all_subject_data, subjects = process.return_data_and_subjects(experiment)

    # make plot dispatcher keys
    # TODO change 'skip' to 'skip' to alter which plots are made
    A = plot_dispatch._make([plot.individual_regressions, 'skip'])
    B = plot_dispatch._make([plot.individual_areas_to_reality, 'skip'])
    C = plot_dispatch._make([plot.individual_areas_between_conditions, 'skip'])
    D = plot_dispatch._make([plot.group_regression_lines_per_condition, 'run'])
    E = plot_dispatch._make([plot.group_areas_per_conditions, 'skip'])
    F = plot_dispatch._make([plot.group_areas_vs_r2_per_condition, 'skip'])
    G = plot_dispatch._make([plot.group_r2_per_condition, 'skip'])
    # Exp1 specific plots
    H = plot_dispatch._make([plot.group_areas_between_conditions, 'skip'])
    I = plot_dispatch._make([plot.group_areas_difference_of_differences, 'skip'])
    # Exp2 specific plots
    J = plot_dispatch._make([plot.lovia_reciprocal_condition_regression, 'skip'])
    K = plot_dispatch._make([plot.slope_comparison, 'skip'])


    # plot according to dispatch keys and experiment
    plot_summary = process.create_plot_dispatcher(experiment, A, B, C, D, E, F, G, H, I, J, K)
    process.plot_by_dispatcher_key(plot_summary, all_subject_data, experiment, subjects)

for experiment in experiments:
    all_subject_data, subjects = process.return_data_and_subjects(experiment)
    plot_journal.example_subjects_group_reg_summary(all_subject_data, subjects, experiment)