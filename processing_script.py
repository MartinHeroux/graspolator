import process

# change string below to match experiment to process
# either 'exp1' or 'exp2' (Kathy and Lovisa respectively)
experiment = 'exp2'

all_subject_data, subjects = process.return_data_and_subjects(experiment)

process.plot_by_dispatcher_key(all_subject_data, experiment, subjects)


subject_ID = 'sub01'
subject_data = all_subject_data[1]
