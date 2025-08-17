import matplotlib.pyplot as plt
import os

def create_single_rmsd_plot_from_file(input_file, output_image_file):
    """
    Reads RMSD values from a text or log file and generates a single
    time-series plot with a 2.0 Ångström threshold line for comparison.

    Args:
        input_file (str): The path to the file containing the RMSD data.
                          It is assumed that each line in the file is a single
                          numerical RMSD value.
        output_image_file (str): The name of the output PNG file for the chart.
    """
    # Check if the input file exists
    if not os.path.exists(input_file):
        print(f"Error: The file '{input_file}' was not found.")
        return

    print(f"Reading RMSD data from '{input_file}'...")
    
    rmsd_values = []
    try:
        with open(input_file, 'r') as f:
            for line in f:
                # Clean up the line (remove whitespace) and convert to a float
                try:
                    rmsd_value = float(line.strip())
                    rmsd_values.append(rmsd_value)
                except ValueError:
                    # Skip lines that can't be converted to a float (e.g., headers or empty lines)
                    continue
    except Exception as e:
        print(f"An error occurred while processing the file: {e}")
        return

    if not rmsd_values:
        print("Error: No valid numerical data found in the input file.")
        return

    # Create a time-step list based on the number of RMSD values found
    time_steps = list(range(len(rmsd_values)))

    # --- GENERATE THE PLOT ---
    plt.style.use('seaborn-v0_8-whitegrid')

    # Create a single figure and axis
    fig, ax = plt.subplots(figsize=(10, 6))

    # Plot the RMSD data
    ax.plot(time_steps, rmsd_values, color='black', label='Protein Backbone RMSD')
    
    # Add the 2.0 Ångström threshold line
    ax.axhline(y=2.0, color='blue', linestyle='--', linewidth=2, label='2.0 Å Threshold')

    # Set labels and title
    ax.set_ylabel('RMSD (angstroms)', fontsize=12)
    ax.set_xlabel('Time (frames)', fontsize=12)
    ax.set_title('Root Mean Square Deviation Over Time', fontsize=14, fontweight='bold')
    
    # Set the x-axis limits
    ax.set_xlim(0, 100)
    
    # Set the y-axis limits to provide better context
    ax.set_ylim(0, max(rmsd_values) + 5 if rmsd_values else 5)
    
    ax.legend(loc='upper right')

    # Adjust layout and save the figure
    plt.tight_layout()
    plt.savefig(output_image_file, dpi=300)

    print(f"Chart successfully saved as '{output_image_file}'")

# --- HOW TO USE ---
if __name__ == "__main__":
   # 1. Name of your input text/log file
    input_file = 'rmsd.log'  # Assumes the file contains a single RMSD value per line
    
    # 2. Name of the output image file
    output_image_file = 'rmsd_chart.png'

    # Run the function to create the chart
    create_single_rmsd_plot_from_file(input_file, output_image_file)
