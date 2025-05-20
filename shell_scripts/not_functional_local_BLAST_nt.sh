#!/bin/bash
## --------------------------
## Job Parameters
## --------------------------
#SBATCH --job-name=local_BLAST_nt   # Job Title
#SBATCH -A node    # Node account
#SBATCH -p bigmem # Big memory partition
#SBATCH --qos normal    # normal priority level

#SBATCH --mem=64G   # request X GB of RAM (memory)
#SBATCH --time=99:00:00    # Running time in HH:MM:SS

#SBATCH --mail-user=adrien.moulart@wsl.ch    # My email
#SBATCH --mail-type=END,FAIL     # Notify me at given events by email


#SBATCH --output=/home/moularta/BLAST/blast_logs/local_BLAST_nt_%j.log     # Standard output or run log (everything that gets printed to console)
#SBATCH --error=/home/moularta/BLAST/blast_logs/local_BLAST_nt_%j.err     # Standard error output or log (only for error messages)


# Load required modules
module load python-3.10.10-gcc-10.2.0-e6k7ynl

# and here, I'm going to load my own python environment (stored in the venv directory, contains libraries like biopython)
source /home/moularta/venv/bin/activate

# ensure the BLAST+ software packages can be located
# this is required by the packages used in the python script
export PATH="/home/moularta/BLAST/ncbi-blast-2.16.0+/bin:$PATH"

# Set the BLASTDB environment variable to point to the local nt database directory
# simply points to where the actual nt database is stored on the HPC
export BLASTDB=/home/moularta/BLAST/complete_blast

# designates the directory that where xml output file will be saved
cd /home/moularta/BLAST/output_xml || exit

# run python script for local BLAST with nt database
python -u /home/moularta/scripts/python_scripts/local_BLAST_nt.py
