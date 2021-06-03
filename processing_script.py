from pathlib import Path
import process
import data_lovisa
import utils_lovisa

#---------------KATHY------------------------------#

all_subject_data_exp1 = process.import_and_parse_data()

process.plot_by_dispatcher_key(all_subject_data_exp1)

#--------------LOVISA-------------------------------#

all_subject_data_lovisa = data_lovisa.process_blocked_data()

subject_data = all_subject_data_lovisa[0]
subject_ID = 'sub01'

experiment = 'exp1'
subjects = utils_lovisa.get_directory_list(Path('./data/exp2'))