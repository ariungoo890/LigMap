#!/bin/bash

#================================================================================
# Improved Ligand Preparation Script
#
# This script prepares a ligand for molecular simulations using Open Babel and MOPAC.
# It handles command-line arguments, validates inputs, and includes robust error checking.
#
# Usage:
#   ./ligand_prep_improved.sh -l <ligand.pdb> -c <charge>
#
# Options:
#   -l, --ligand      Path to the input ligand PDB file.
#   -c, --charge      The expected total charge of the ligand.
#================================================================================

# --- Initialize variables ---
input_ligand_pdb=""
expected_charge=""
ligand_name=""

# --- Function to check if a command exists ---
command_exists () {
  command -v "$1" >/dev/null 2>&1
}

# --- Check for required programs ---
echo "Checking for required programs..."
if ! command_exists "obabel"; then
  echo "Error: Open Babel (obabel) is not found. Please install it or add it to your PATH."
  exit 1
fi

# Use the full path for MOPAC
MOPAC_EXE='/opt/mopac/MOPAC2016.exe'
if [ ! -f "$MOPAC_EXE" ]; then
  echo "Error: MOPAC executable '$MOPAC_EXE' not found."
  exit 1
fi
echo "All required programs found."

# --- Parse command-line arguments ---
while [[ "$#" -gt 0 ]]; do
  case "$1" in
    -l|--ligand)
      if [ -f "$2" ]; then
        input_ligand_pdb="$2"
        ligand_name=$(basename "${input_ligand_pdb%.*}")
      else
        echo "Error: Ligand file '$2' not found."
        exit 1
      fi
      shift # past argument
      shift # past value
      ;;
    -c|--charge)
      expected_charge="$2"
      shift # past argument
      shift # past value
      ;;
    *)
      # Unknown option
      echo "Unknown option: $1"
      exit 1
      ;;
  esac
done

# --- Validate required arguments ---
if [ -z "$input_ligand_pdb" ] || [ -z "$expected_charge" ]; then
  echo "Usage: $0 -l <ligand.pdb> -c <charge>"
  exit 1
fi

echo "--- Starting ligand preparation for $input_ligand_pdb ---"
echo ""

# --- Step 1: Convert PDB to MOL2 and Add Hydrogens ---
echo "Step 1: Converting PDB to MOL2 and adding hydrogens..."
output_mol2="${ligand_name}_h.mol2"
obabel -ipdb "$input_ligand_pdb" -omol2 -O "$output_mol2" --addH
if [ ! -f "$output_mol2" ]; then
  echo "Error: Failed to create MOL2 file."
  exit 1
fi
echo "Success: Created $output_mol2."

# --- Step 2: Validate Ligand Charge ---
echo ""
echo "Step 2: Validating ligand charge..."
# Use awk to sum the 9th column (charge) of the atom records
calculated_charge=$(grep 'UNL1' "$output_mol2" | awk '{sum+=$9} END{print sum}')
# Round the calculated charge to the nearest integer
calculated_charge_int=$(printf "%.0f\n" "$calculated_charge")

if [ "$calculated_charge_int" -ne "$expected_charge" ]; then
  echo "Error: The calculated charge ($calculated_charge_int) does not match the user provided charge ($expected_charge)."
  echo "Please check the charge and the input PDB file."
  exit 1
fi
echo "Success: Ligand charge ($calculated_charge_int) matches the expected charge ($expected_charge)."

# --- Step 3: Perform Open Babel Energy Minimization ---
echo ""
echo "Step 3: Performing Open Babel energy minimization (MMFF94)..."
obminimize -omol2 -ff mmff94 -n 100000 -sd "$output_mol2" > "${ligand_name}_h_sd.mol2"
if [ ! -f "${ligand_name}_h_sd.mol2" ]; then
  echo "Error: Failed to perform steepest descent minimization."
  exit 1
fi
echo "Success: Steepest descent minimization complete."

obminimize -omol2 -ff mmff94 -n 10000 -c 1e-7 -cg "${ligand_name}_h_sd.mol2" > "${ligand_name}_h_cg.mol2"
if [ ! -f "${ligand_name}_h_cg.mol2" ]; then
  echo "Error: Failed to perform conjugate gradient minimization."
  exit 1
fi
echo "Success: Conjugate gradient minimization complete."

# --- Step 4: Perform MOPAC Semi-Empirical Optimization ---
echo ""
echo "Step 4: Performing MOPAC semi-empirical optimization..."
obabel -imol2 "${ligand_name}_h_cg.mol2" -omop -O "${ligand_name}_h.mop"
if [ ! -f "${ligand_name}_h.mop" ]; then
  echo "Error: Failed to create MOPAC input file."
  exit 1
fi

# Use sed to add the necessary keywords and charge
sed -i "s/PUT KEYWORDS HERE/PM7 PREC DENSITY MULLIK EF GNORM=0.001 LET PRECISE CHARGE=${expected_charge}/" "${ligand_name}_h.mop"

"$MOPAC_EXE" "${ligand_name}_h.mop"
if [ ! -f "${ligand_name}_h.arc" ]; then
  echo "Error: MOPAC job failed. The .arc file was not created."
  exit 1
fi
echo "Success: MOPAC job completed."

# --- Step 5: Convert MOPAC Output to Final PDB ---
echo ""
echo "Step 5: Converting MOPAC output to final PDB file..."
# Extract optimized geometry from the .arc file
sed '1,39d' "${ligand_name}_h.arc" > "${ligand_name}_F.mop"
if [ ! -f "${ligand_name}_F.mop" ]; then
  echo "Error: Failed to extract geometry from MOPAC .arc file."
  exit 1
fi

obabel -imop "${ligand_name}_F.mop" -opdb -O "${ligand_name}_opt.pdb"
if [ ! -s "${ligand_name}_opt.pdb" ]; then
  echo "Error: Final PDB file not created or is empty. Ligand preparation failed."
  exit 1
fi
echo "Success: Final optimized PDB file created: ${ligand_name}_opt.pdb."

echo ""
echo "✨ Ligand preparation was successful! ✨"
