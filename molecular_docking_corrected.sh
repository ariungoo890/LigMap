#!/bin/bash
#================================================================================
# Usage:
#   ./molecular_docking_corrected.sh -i <input.log> -l <ligand_opt.pdb>
#
# Options:
#   -i, --input_log_file      The input log file.
#   -l, --ligand_opt.pdb      The path to ligand_opt.pdb generated from ligand_prep_corrected.py
#================================================================================

# --- Functions ---
command_exists () {
  command -v "$1" >/dev/null 2>&1
}

# --- Check for required programs ---
echo "Checking for required programs..."
if ! command_exists "autodock4" || ! command_exists "autogrid4"; then
  echo "Error: autodock4 and/or autogrid4 not found. Please install them or add them to your PATH."
  exit 1
fi

# --- Parse command-line arguments ---
input_log_file=""
while [[ "$#" -gt 0 ]]; do
  case "$1" in
    -i|--input_log_file)
      if [ -f "$2" ]; then
        input_log_file="$2"
      else
        echo "Error: Input log file '$2' not found."
        exit 1
      fi
      shift; shift
      ;;
    -l|--ligand_opt_pdb_path)
    ligand_opt_pdb_path="$2"
    shift # past argument
    shift # past value
      ;;
    *)
      echo "Error: Unknown parameter passed: $1"
      exit 1
      ;;
  esac
done

if [ -z "$input_log_file" ]; then
  echo "Error: An input log file is required. Use -i or --input_log_file."
  exit 1
fi

# --- File paths ---
TARGETS_DIR="/home/bayar/Documents/input/target_holo"
GRID_INFO_FILE="/home/bayar/Documents/input/target_holo/grid_cal_info.txt"
AUTODOCK_BIN_DIR="/home/bayar/bin"

# Get ligand and target info from the input log file
#ligand_opt_pdb_path=$(grep "Ligand_input_path:" "$input_log_file" | awk '{print $2}')
ligand_name=$(basename "${ligand_opt_pdb_path%.*}")
targets=$(grep "Target_selection:" "$input_log_file" | awk -F': ' '{print $2}')
targets_array=($targets)

echo "Using ligand: $ligand_opt_pdb_path"
echo "Targets selected: ${targets_array[@]}"

# --- Prepare ligand PDBQT file once ---
echo "Preparing ligand PDBQT..."
pythonsh "${AUTODOCK_BIN_DIR}/prepare_ligand4.py" -l "$ligand_opt_pdb_path" -o "${ligand_name}.pdbqt" -v -d "${AUTODOCK_BIN_DIR}/ligand_dict.py" -F
echo "Ligand PDBQT file created: ${ligand_name}.pdbqt"

# --- Main Docking Loop ---
for target_pdb_id in "${targets_array[@]}"; do
  echo "-----------------------------------"
  echo "Processing target: $target_pdb_id"

  input_target_pdb="${TARGETS_DIR}/${target_pdb_id}.pdb"
  target_name=$(basename "${input_target_pdb%.*}")

  # Prepare receptor PDBQT file
  echo "Preparing receptor PDBQT for $target_name..."
  pythonsh "${AUTODOCK_BIN_DIR}/prepare_receptor4.py" -r "$input_target_pdb" -o "${target_name}.pdbqt" -v -U nphs
  
  # Get grid information for the current target from grid_cal_info.txt
  grid_info=$(grep -w "$target_pdb_id" "$GRID_INFO_FILE")
  if [[ -z "$grid_info" ]]; then
    echo "Error: Grid information for $target_pdb_id not found."
    continue
  fi

  x=$(echo "$grid_info" | awk '{print $2}')
  y=$(echo "$grid_info" | awk '{print $3}')
  z=$(echo "$grid_info" | awk '{print $4}')
  npts_val=$(echo "$grid_info" | awk '{print $5}')
  
  npts_str="$npts_val,$npts_val,$npts_val"
  gridcenter_str="$x,$y,$z"

  echo "Grid center: $gridcenter_str, npts: $npts_str"
  
  # Prepare grid parameter file (GPF)
  echo "Preparing GPF for $target_name..."
  pythonsh "${AUTODOCK_BIN_DIR}/prepare_gpf4.py" -l "${ligand_name}.pdbqt" -r "${target_name}.pdbqt" -o "grid_${target_name}.gpf" -p spacing=0.375 -p npts="$npts_str" -p gridcenter="$gridcenter_str"
  
  # Run grid calculation
  echo "Running autogrid4 for $target_name..."
  autogrid4 -p "grid_${target_name}.gpf" -l "grid_${target_name}.glg"

  # Prepare docking parameter file (DPF)
  echo "Preparing DPF for $target_name..."
  pythonsh "${AUTODOCK_BIN_DIR}/prepare_dpf42.py" -l "${ligand_name}.pdbqt" -r "${target_name}.pdbqt" -o "docking_${target_name}.dpf" -p ga_num_evals=25000000 -p ga_pop_size=150 -p ga_num_generations=10000000 -p ga_run=50 -p rmstol=2
  
  # Run docking calculation
  echo "Running autodock4 for $target_name..."
  autodock4 -p "docking_${target_name}.dpf" -l "docking_${target_name}.dlg"
  
  # Evaluate docking results using pantools
  echo "Evaluating docking results for $target_name..."
  pantools -o "docking_${target_name}.dlg"
  echo "Finished processing target: $target_pdb_id"

  # Remove intermediate files for this target.
  echo "Cleaning up intermediate files for $target_name..."
  rm -f "${target_name}.pdbqt" "grid_${target_name}.gpf" "grid_${target_name}.glg" "docking_${target_name}.dpf" "docking_${target_name}.dlg" *.map *.fld *.xyz
  echo "-----------------------------------"
done

echo "All targets processed."

# --- Final file selection and cleanup ---
dgmin_threshold=-7
selected_targets_log="docking_selected_targets.log"
echo "Selected Targets and their dGmin values" > "$selected_targets_log"
echo "---------------------------------------" >> "$selected_targets_log"

targets=$(grep "Target_selection:" "$input_log_file" | awk -F': ' '{print $2}')
targets_array=($targets)

for target in "${targets_array[@]}"; do
    sta_file="O_docking_${target}.sta"
    pdb_file="O_docking_${target}_rank_1.pdb"
    
    if [[ ! -f "$sta_file" ]]; then
        echo "Warning: $sta_file not found. Skipping."
        continue
    fi

    # Read the dGmin value for Rank 1 from the file.
    dgmin_value=$(grep -A1 '#Rank' "$sta_file" | tail -n 1 | awk '{print $2}')

    if (( $(echo "$dgmin_value < $dgmin_threshold" | bc -l) )); then
        echo "Target $target with dGmin $dgmin_value meets the criteria."
        echo "$target: $dgmin_value" >> "$selected_targets_log"
    else
        echo "Target $target with dGmin $dgmin_value does not meet the criteria. Deleting files."
        rm -f "$sta_file" "$pdb_file"
    fi
done

# Remove the ligand PDBQT file at the very end
rm -f "${ligand_name}.pdbqt"

echo "Final selection process complete."