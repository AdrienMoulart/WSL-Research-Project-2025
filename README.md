This project contains the tools I used to complete my research project at the WSL in Birmensdorf (Zürich, Switzerland), the goal of which is to perform data analysis on data trends within the database generated from 2016 to 2024 by the diagnostics and forest protection research groups.

The main_wsl_project_notebook contains the steps I took to work on the PHP_diagnostics_2016_2024 database from the diagnostics team led by Simone Prospero, up to the generation of the sequence_analysis_data file that served as a transition to my second notebook dedicated to the BLAST search.

The BLAST_notebook.ipynb file contains my work on an automated blast pipeline for a local BLAST search ran on a high performance computing cluster (such as Hyperion at WSL). The python and shell scripts contained in this project should be enough to reproduce all my methods that led to the results found within the notebook, provided that the environment structure is adapted first.

All package information as well as the python version can be found in the conda_envrionment.yml file in project_information/.
