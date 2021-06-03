from pathlib import Path

import data_lovisa

data_folder = Path('./data/exp2')

parsed_group_data = data_lovisa.process_blocked_data(data_folder)

subject_data = parsed_group_data[1]


