import process

all_subject_data = process.import_and_parse_data()

process.plot_by_dispatcher_key(all_subject_data)