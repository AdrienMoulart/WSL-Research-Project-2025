#!/bin/bash
## --------------------------
## Job Parameters
## --------------------------
#SBATCH --job-name=extract_blast_results_from_xml   # Job Title
#SBATCH -A node    # Node account
#SBATCH -p bigmem # Big memory partition
#SBATCH --qos normal    # normal priority level

#SBATCH --mem=64G   # request X GB of RAM (memory)
#SBATCH --time=72:00:00    # Running time in HH:MM:SS

#SBATCH --mail-user=adrien.moulart@wsl.ch    # My email
#SBATCH --mail-type=END,FAIL     # Notify me at given events by email


#SBATCH --output=/home/moularta/BLAST/blast_logs/extract_blast_results_from_xml_%j.log     # Standard output or run log (everything that gets printed to console), %j adds job ID
#SBATCH --error=/home/moularta/BLAST/blast_logs/extract_blast_results_from_xml_%j.err     # Standard error output or log (only for error messages)


# Load required modules
module load python-3.10.10-gcc-10.2.0-e6k7ynl

# and here, I'm going to load my own python environment (stored in the venv directory, contains libraries like biopython)
source /home/moularta/venv/bin/activate

# run python script for local BLAST with nt database
# -u is very important (it stands for unbuffered) as it allows us to read print statements in the log file (which tend to vanish otherwise)
python -u /home/moularta/scripts/python_scripts/extract_blast_results_from_xml.py
