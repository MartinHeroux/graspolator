## Graspolator 
***
Code and data for the Graspolator manuscript.

In the study manuscript, Experiment 1 was conducted by Lovisa, and Experiment 2 was conducted by Kathy.

However, Kathy collected data before Lovisa. 

As such:
- Functions in ```run_exp1.py``` and ```run_exp2.py``` are named according to the experimental order reported in the manuscript (Exp1 = Lovisa, Exp2 = Kathy).
- Back-end functions are named according to the chronological order of the experiments, or according to the person who conducted the study (Exp1 = Kathy, Exp2 = Lovisa).
- Results are saved according to the order reporting in the manuscript (e.g. exp1_results.txt == Lovisa study)

### Requirements
***
- Python 3
- Package requirements as saved in requirements.txt

### Installation
***
```
$ cd ../path/to/project/directory
$ git clone https://github.com/MartinHeroux/graspolator.git
$ pip install -r requirements.txt
```

### Data location
***
X:\Projects\3 PROPRIOPCEPTION\PROPRIO_GRASPOLATOR\data\raw_data

### Usage
***
While in the project directory:
- To process and export results and figures for Exp 1 run the following in the terminal:

    ```$ python run_exp1.py```
- To process and export results and figures for Exp 2 run the following in the terminal:

    ```$ python run_exp2.py```


### Outputs
***
The following subdirectories will be created in the project directory:
- ./results
- ./figures
- ./data
- ./plots

For Exp 1 (Lovisa), the following files will be created:
- ./results/results_exp1.txt
- ./plots/individual_plots/error_plots_exp1/participant_ID.png (1 x  for each participant)
- ./plots/individual_plots/scatterplots_exp1/participant_ID.png (1 x  for each participant)
- ./figures/Figure_2.png
- ./figures/Figure_2.svg
- ./figures/Figure_3.png
- ./figures/Figure_3.svg
- ./figures/Figure_4.png
- ./figures/Figure_4.svg
- ./figures/Figure_5.png
- ./figures/Figure_5.svg
- ./data/summary_data/participant_data_summary_exp1_lovisa.csv

For Exp 2 (Kathy), the following files will be created:
- ./results/results_exp2.txt
- ./plots/individual_plots/error_plots_exp2/participant_ID.png (1 x  for each participant)
- ./plots/individual_plots/scatterplots_exp2/participant_ID.png (1 x  for each participant)
- ./figures/Figure_6.png
- ./figures/Figure_6.svg
- ./figures/Figure_7.png
- ./figures/Figure_7.svg
- ./figures/Figure_8.png
- ./figures/Figure_8.svg
- ./data/summary_data/participant_data_summary_exp2_kathy.csv
