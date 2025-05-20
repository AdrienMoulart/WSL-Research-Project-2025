#!/bin/bash

## --------------------------
## Job Parameters
## --------------------------
#SBATCH --job-name=blastdb_extract   # Job Title
#SBATCH -A node    # Node account
#SBATCH -p bigmem # Big memory partition
#SBATCH --qos normal    # normal priority level
#SBATCH --mail-user=adrien.moulart@wsl.ch    # My email
#SBATCH --mail-type=END,FAIL     # Notify me at given events by email
#SBATCH -o blastdb_extract_%j.log     # Standard output or run log (everything thats gets printed to console)
#SBATCH -e blastdb_extract_%j.err     # Standard error output or log (only for error msgs)
#SBATCH --mem=40000M   # request X GB of RAM (memory)
#SBATCH --time=03:00:00    # Running time in HH:MM:SS


# Load the Perl module
# we will use the one from linux-centos7-x86_64, which seems to be a generic optimization. (this is because I don't know the HPC micro architecture)
module load perl-5.26.2-gcc-4.8.5-hnx5wqj

# Change directory to where the tar.gz files are located.
# Replace /path/to/uncompressed_blast_db with the correct directory.
cd /home/moularta/BLAST/complete_blast

echo "Starting extraction of BLAST database segments..."
for file in *.tar.gz; do
    echo "Extracting $file ..."
    tar -xzf "$file"
done

echo "Extraction complete."
