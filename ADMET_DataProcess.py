import csv
import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def generate_admet_radar_chart(input_csv_path, output_png_path):
    """
    Reads an ADMET predictions CSV, extracts specific properties, renames them,
    and generates a radar chart, saving it as a PNG file.

    Args:
        input_csv_path (str): Path to the input CSV file (e.g., admet_predicts.csv).
        output_png_path (str): Path to save the output radar chart PNG.
    """
    # --- Part 1: Data Extraction and Renaming (from data_extract_renaming.py) ---

    # Define the mapping from desired short names to the long names in the CSV header
    property_mapping = {
        "Lipinski": "Lipinski_drugbank_approved_percentile",
        "hERG Safe": "hERG_drugbank_approved_percentile",
        "Bioavailable": "Bioavailability_Ma_drugbank_approved_percentile",
        "Soluble": "Solubility_AqSolDB_drugbank_approved_percentile",
        "Non-Toxic": "ClinTox_drugbank_approved_percentile"
    }
    csv_property_names = list(property_mapping.values())
    
    # Check if the input file exists before proceeding
    if not os.path.exists(input_csv_path):
        print(f"Error: The file '{input_csv_path}' was not found.")
        return

    print(f"Reading and processing data from '{input_csv_path}'...")
    
    extracted_data = []
    try:
        with open(input_csv_path, 'r', newline='') as infile:
            reader = csv.reader(infile)
            header_row = next(reader)
            
            # Find the indices of the desired properties in the header
            property_indices = []
            for prop in csv_property_names:
                try:
                    property_indices.append(header_row.index(prop))
                except ValueError:
                    print(f"Warning: The property '{prop}' was not found in the header.")
            
            if not property_indices:
                print("Error: No valid properties were found in the CSV header.")
                return

            # Read the first data row and extract the desired values
            data_row = next(reader)
            extracted_values = [data_row[i] for i in property_indices]
            
            # Get the new, shorter header names in the correct order
            new_header = [list(property_mapping.keys())[i] for i, long_name in enumerate(csv_property_names) if long_name in header_row]
            
            # Combine the new headers and extracted values into a dictionary
            # This is a good intermediate step for clarity
            extracted_data = dict(zip(new_header, extracted_values))

    except FileNotFoundError:
        print(f"Error: The file '{input_csv_path}' was not found.")
        return
    except StopIteration:
        print("Error: The input CSV file appears to be empty or missing data rows.")
        return
    except Exception as e:
        print(f"An unexpected error occurred during data extraction: {e}")
        return

    # --- Part 2: Radar Chart Generation (from admet_radar_chart.py) ---
    print("Data processed. Generating radar chart...")

    # Load the extracted data into a pandas DataFrame
    df = pd.DataFrame([extracted_data])
    
    # Extract feature names and values from the DataFrame
    features = list(df.columns)
    values = df.iloc[0].values.flatten().tolist()
    
    # Ensure the values are within the specified range [0, 100]
    values = [min(max(float(val), 0), 100) for val in values]
    
    # A radar chart is a polar plot with a specific number of axes
    N = len(features)
    angles = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist()
    
    # The plot is a circle, so the first point must be repeated to close the loop
    values += values[:1]
    angles += angles[:1]
    
    # Create the plot
    fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(polar=True))
    ax.plot(angles, values, color='blue', linewidth=2)
    ax.fill(angles, values, color='blue', alpha=0.25)
    
    # Set the limits of the y-axis
    ax.set_ylim(0, 100)
    
    # Set the angle of the axis labels
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(features, size=13, ha='left')
    
    # Set the title
    plt.title('ADMET Predictions Radar Chart', size=15, color='black', y=1.1)
    
    # Save the figure
    plt.savefig(output_png_path)
    
    print(f"Successfully generated the radar chart and saved it to: '{output_png_path}'")
    print("Processing complete.")


# --- HOW TO USE ---
if __name__ == "__main__":
    # 1. Change this to the name of your input CSV file
    input_file = 'admet_predicts.csv'
    
    # 2. This will be the name of the new PNG file created by the script
    output_image_file = 'admet_radar_chart.png'
    
    # 3. Run the main function
    generate_admet_radar_chart(input_file, output_image_file)