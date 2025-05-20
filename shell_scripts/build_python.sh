#!/bin/bash

## --------------------------
## Job Parameters
## --------------------------
#SBATCH --job-name=build_python   # Job Title
#SBATCH -A node    # Node account
#SBATCH -p node # Big memory partition
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


# This script downloads, builds, and installs Python 3.12.9 from source code available online.

# where I want my installation
cd /home/moularta/software/python_builds || exit

# Download the Python 3.12.9 source tarball
wget https://www.python.org/ftp/python/3.12.9/Python-3.12.9.tgz

# Extract the tarball
tar -xzf Python-3.12.9.tgz

# Change into the extracted directory
cd Python-3.12.9 || exit

# now, importantly, we need to mark the location of openssl and libffi to make them available to the installation process
# this is because I manually installed them and they are sitting in a custom directory within my software dir
# the -WL, -rpath option is what I saw recommended with regards to fixing the issue of installations not automatically looking for this sometimes, so I've included it here.
export CPPFLAGS="-I/home/moularta/software/libffi/include -I/home/moularta/software/open_ssl/include"
export LDFLAGS="-L/home/moularta/software/libffi/lib -L/home/moularta/software/open_ssl/lib -Wl,-rpath,/home/moularta/software/open_ssl/lib"

# Configure the build; --prefix sets the installation directory.
# --enable-optimizations enables extra optimizations (this makes the build slower but results in a faster Python).
# we also use open ssl during the installation process so we add our custom version here as a python installation option
./configure --prefix=/home/moularta/python3.12.9 --enable-optimizations --with-openssl=/home/moularta/software/open_ssl


# Build Python using 8 cores
# adjust -j flag based on available cores, here using 8 out of what should be 12 available ones
make -j 8

# Install Python into the specified prefix directory
make install

echo "Python 3.12.9 has been installed in /home/moularta/python3.12.9/bin"
