import plot_journal
import utils

experiments = ['exp1', 'exp2']


for experiment in experiments:
    all_subject_data, subjects = utils.return_data_and_subjects(experiment)

    plot_journal.example_subjects_group_reg_summary(all_subject_data, subjects, experiment)
    plot_journal.r2_area_plots(all_subject_data, subjects, experiment)

    if experiment == 'exp1':
        plot_journal.consistency_between_conditions(all_subject_data, experiment)

    if experiment == 'exp2':
        plot_journal.slope_comparison(all_subject_data, experiment)
        plot_journal.area_vs_r2_plot(all_subject_data, experiment)
