#!/bin/bash

# --- ADMET-AI HPC Installation Script ---
# This script is tailored for use on a high-performance computing cluster.
# It sets up a Conda environment and installs ADMET-AI and its dependencies.

# Exit immediately if a command exits with a non-zero status.
set -e

# --- Script Configuration ---
# You can change these variables if needed
ENV_NAME="admet_ai"
PYTHON_VERSION="3.10"
REPO_URL="https://github.com/swansonk14/admet_ai.git"
REPO_DIR="admet_ai"
INSTALL_DIR=$(pwd) # Installation will happen in the current directory

echo "Starting ADMET-AI installation script for HPC..."
echo "Installation Directory: ${INSTALL_DIR}"
echo "------------------------------------------------"

# --- Step 1: Load Conda Module (if applicable) ---
# Many HPC systems require loading Conda through a module system.
# Uncomment the line below if your system uses 'module load'.
# module load anaconda3

# Check if conda is available
if ! command -v conda &> /dev/null
then
    echo "Error: conda could not be found. Please ensure it is in your PATH or loaded via a module."
    exit 1
fi

# --- Step 2: Create and Activate Conda Environment ---
echo "1. Creating Conda environment '${ENV_NAME}' with Python ${PYTHON_VERSION}..."
conda create -y -n "${ENV_NAME}" python="${PYTHON_VERSION}"

echo "Activating environment '${ENV_NAME}'..."
# This command is necessary to correctly activate Conda environments in scripts
# and is standard practice on HPC systems.
source "$(conda info --base)/etc/profile.d/conda.sh"
conda activate "${ENV_NAME}"

# --- Step 3: Clone the Repository ---
echo "2. Cloning ADMET-AI repository from GitHub..."
# Check if the directory already exists to prevent an error if the script is run again.
if [ -d "${REPO_DIR}" ]; then
    echo "Directory '${REPO_DIR}' already exists. Skipping clone."
else
    git clone "${REPO_URL}"
fi

# --- Step 4: Install Dependencies ---
echo "3. Navigating to project directory '${REPO_DIR}' and installing dependencies..."
cd "${REPO_DIR}"

# Install the package in "editable" mode along with its core dependencies.
pip install -e .

# Install a specific package that was causing issues.
echo "Installing pandas..."
pip install pandas

# This command will install/update all dependencies from the requirements file.
# Make sure your requirements.txt file in the repository is up-to-date with your desired versions.
echo "Installing/Updating dependencies from requirements.txt..."
pip install -r requirements.txt

echo "torch==2.5.0" >> requirements.txt
pip install -r requirements.txt

echo "------------------------------------------------"
echo "✅ ADMET-AI installation complete!"
echo ""
echo "To use the ADMET-AI environment in a job submission script (e.g., Slurm or PBS), you would use the following commands:"
echo "  source "$(conda info --base)/etc/profile.d/conda.sh""
echo "  conda activate ${ENV_NAME}"
echo "  # Your Python script command here"
echo ""
echo "The environment is now ready for use on the cluster."
