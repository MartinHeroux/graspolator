from pathlib import Path

import data
import figures
import plot
import results
from utils import ExpCodes

##########################
#   EXPERIMENT 1 - LOVISA
##########################
import summarise

exp_1 = ExpCodes.EXP_1
exp_1_data_directory = Path(f"./data/{exp_1}'")

#   Store subject data and subject names
all_subject_data_exp1 = data.return_all_subject_data(
    exp_1, exp_1_data_directory
)
all_subject_names_exp1 = data.return_all_subject_IDs(exp_1, exp_1_data_directory)

#   Write results to text file
results.write_all(all_subject_data_exp1, all_subject_names_exp1, exp_1, exp_1_data_directory)

#   Write individual subject data to .csv
summarise.write_raw_data_summary_exp1(all_subject_data_exp1)

#   Generate individual subject plots
plot.individual_scatterplots(all_subject_data_exp1, all_subject_names_exp1, exp_1)
plot.individual_error_plots(all_subject_data_exp1, all_subject_names_exp1, exp_1)

#   Generate figures
figures.generate_all(all_subject_data_exp1, all_subject_names_exp1, exp_1, True)


############################
#   EXPERIMENT 2 - KATHY
############################
exp_2 = ExpCodes.EXP_2
exp2_data_directory = Path(f"./data/{exp_2}")

#   Store subject data and subject names
all_subject_data_exp2 = data.return_all_subject_data(
    exp_2, exp2_data_directory
)
all_subject_names_exp2 = data.return_all_subject_IDs(exp_2, exp2_data_directory)

#   Write results to text file
results.write_all(all_subject_data_exp2, all_subject_names_exp2, exp_2, exp2_data_directory)

#   Write individual subject data to .csv
summarise.write_raw_data_summary_exp2(all_subject_data_exp2, all_subject_names_exp2)

#   Generate individual subject plots
plot.individual_scatterplots(all_subject_data_exp2, all_subject_names_exp2, exp_2)
plot.individual_error_plots(all_subject_data_exp2, all_subject_names_exp2, exp_2)

#   Generate figures
figures.generate_all(all_subject_data_exp2, all_subject_names_exp2, exp_2, True)
