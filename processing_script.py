from pathlib import Path
import process
import data_lovisa

#---------------KATHY------------------------------#

all_subject_data_kathy = process.import_and_parse_data()

process.plot_by_dispatcher_key(all_subject_data_kathy)

#--------------LOVISA-------------------------------#

all_subject_data_lovisa = data_lovisa.process_blocked_data()

