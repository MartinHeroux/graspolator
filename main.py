from pathlib import Path

from data_lovisa import get_lovisa_data
from data_kathy import get_kathy_data
import results_kathy
import results_lovisa
import figure2
import figure3
import figure4
import figure5
import figure6
import figure7
import figure8

# -----------------------------------------------------------------------------
# LOVISA STUDY
# -----------------------------------------------------------------------------
data_folder = Path(f"./data/exp2")
study_data = get_lovisa_data(data_folder)

plot_outcomes = results_lovisa.numerical(study_data, data_folder)
figure2.plot(study_data)
figure3.plot(study_data, plot_outcomes[0])
figure4.plot(plot_outcomes[1])
figure5.plot(plot_outcomes[2])

# -----------------------------------------------------------------------------
# KATHY STUDY
# -----------------------------------------------------------------------------
data_folder = Path(f"./data/exp1")
study_data = get_kathy_data(data_folder)

plot_outcomes = results_kathy.numerical(study_data, data_folder)
figure6.plot(study_data)
figure7.plot(study_data, plot_outcomes[0])
figure8.plot(plot_outcomes[1:])
