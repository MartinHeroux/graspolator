from pathlib import Path

import data
import figures
import plot
import results

#####################
#   EXPERIMENT 1
#####################
exp_1 = "exp2"
exp_1_data_directory = Path("./data/exp2")

#   Store all subject data and subject names
all_subject_data_exp1 = data.return_all_subject_data(
    exp_1, exp_1_data_directory
)
all_subject_names_exp1 = data.return_all_subject_IDs(exp_1, exp_1_data_directory)

#   Write all results to text file
results.write_all(all_subject_data_exp1, all_subject_names_exp1, exp_1, exp_1_data_directory)

#   Generate individual subject plots
plot.individual_scatterplots(all_subject_data_exp1, all_subject_names_exp1, exp_1)
plot.individual_error_plots(all_subject_data_exp1, all_subject_names_exp1, exp_1)

#   Generate all figures
figures.generate_all(all_subject_data_exp1, all_subject_names_exp1, exp_1)


#####################
#   EXPERIMENT 2
#####################
exp_2 = "exp1"
exp_2_data_directory = Path("./data/exp1")
exp_2_result_filepath = Path("./results_exp1.txt")

#   Store all subject data and subject names
all_subject_data_exp2 = data.return_all_subject_data(
    exp_2, exp_2_data_directory
)
all_subject_names_exp2 = data.return_all_subject_IDs(exp_2, exp_2_data_directory)

#   Write all results to text file
results.write_all(all_subject_data_exp2, all_subject_names_exp2, exp_2, exp_2_data_directory)

#   Generate individual subject plots
plot.individual_scatterplots(all_subject_data_exp2, all_subject_names_exp2, exp_2)
plot.individual_error_plots(all_subject_data_exp2, all_subject_names_exp2, exp_2)

#   Generate all figures
figures.generate_all(all_subject_data_exp2, all_subject_names_exp2, exp_2)
