#!/bin/bash

## --------------------------
## Job Parameters
## --------------------------
#SBATCH --job-name=build_python   # Job Title
#SBATCH -A node    # Node account
#SBATCH -p node # memory partition
#SBATCH --qos normal    # normal priority level
#SBATCH --mail-user=adrien.moulart@wsl.ch    # My email
#SBATCH --mail-type=END,FAIL     # Notify me at given events by email
#SBATCH -o build_python_%j.log     # Standard output or run log (everything thats gets printed to console)
#SBATCH -e build_python_%j.err     # Standard error output or log (only for error msgs)
#SBATCH --mem=32G   # request X GB of RAM (memory)
#SBATCH --time=03:00:00    # Running time in HH:MM:SS

# experimental parameters for software building
# should be fine as the hyperion cluster seems to have 12 cores available
# basing this on running nproc from home
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8


# This script downloads, builds, and installs the open ssl version 1.1.1u (needed to install python)

# where I want my installation
cd /home/moularta/software/open_ssl || exit

# Download the openssl source tarball
wget https://www.openssl.org/source/openssl-1.1.1u.tar.gz

# decompress tarball
tar -xzf openssl-1.1.1u.tar.gz

# Change into the extracted directory
cd openssl-1.1.1u || exit

# Configure the build
# --prefix sets the installation directory.
./config --prefix=/home/moularta/software/open_ssl --openssldir=/home/moularta/software/open_ssl

# Build openssl using x cores
# adjust -j flag based on available cores, here using 8 out of what should be 12 available ones
make -j 8

# Install openssl into the specified prefix directory
make install

echo "Openssl has been installed."
