#!/bin/bash
# load_modules.sh - Loads my preferred HPC modules automatically

# Load the Perl module
# we will use the one from linux-centos7-x86_64, which seems to be a generic optimization. (this is because I don't know the HPC micro architecture)
module load perl-5.26.2-gcc-4.8.5-hnx5wqj


# Load additional modules here as needed
# For example:
# module load ncbi-blast/2.16.0+
# module load python/3.8.5

echo "Preferred modules loaded."
