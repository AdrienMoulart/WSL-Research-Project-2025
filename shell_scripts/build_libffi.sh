#!/bin/bash

## --------------------------
## Job Parameters
## --------------------------
#SBATCH --job-name=build_libffi   # Job Title
#SBATCH -A node    # Node account
#SBATCH -p node # memory partition
#SBATCH --qos normal    # normal priority level
#SBATCH --mail-user=adrien.moulart@wsl.ch    # My email
#SBATCH --mail-type=END,FAIL     # Notify me at given events by email
#SBATCH -o build_libffi_%j.log     # Standard output or run log (everything thats gets printed to console)
#SBATCH -e build_libffi_%j.err     # Standard error output or log (only for error msgs)
#SBATCH --mem=32G   # request X GB of RAM (memory)
#SBATCH --time=03:00:00    # Running time in HH:MM:SS

# experimental parameters for software building
# should be fine as the hyperion cluster seems to have 12 cores available
# basing this on running nproc from home
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8


# This script downloads, builds, and installs the libffi-3.4.2 (a library needed to install python)

# where I want my installation
cd /home/moularta/software/libffi || exit

# Download the libffi source tarball
wget https://github.com/libffi/libffi/releases/download/v3.4.2/libffi-3.4.2.tar.gz

# decompress tarball
tar -xzf libffi-3.4.2.tar.gz

# Change into the extracted directory
cd libffi-3.4.2 || exit

# Configure the build
# --prefix sets the installation directory.
# apparently libffi uses configure instead of config which proke the installation initially so careful with that
./configure --prefix=/home/moularta/software/libffi

# Build libffi using x cores
# adjust -j flag based on available cores, here using 8 out of what should be 12 available ones
make -j 8

# Install libffi into the specified prefix directory
make install

echo "libffi has been installed."
