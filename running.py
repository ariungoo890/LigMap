#!/usr/bin/env python3
import subprocess
import os
import sys
import platform
from pathlib import Path

# ==== Step 0: Ensure required packages are installed ====
def install_packages(packages):
    for pkg in packages:
        subprocess.run([sys.executable, "-m", "pip", "install", pkg], check=True)

required_packages = ["pandas", "reportlab", "pillow"]
install_packages(required_packages)

import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch

# ==== Step 1: Locate 'admet_ai' Conda environment Python ====
try:
    conda_base = subprocess.check_output(["conda", "info", "--base"], text=True).strip()
except subprocess.CalledProcessError:
    print("❌ Conda is not installed or not in PATH.")
    sys.exit(1)

admet_ai_python = os.path.join(conda_base, "envs", "admet_ai", "bin", "python")
if not os.path.isfile(admet_ai_python):
    print(f"❌ Could not find Python in 'admet_ai' environment: {admet_ai_python}")
    sys.exit(1)

# ==== Step 2: Run ADMET prediction scripts ====
def run_script(script_name):
    if os.path.isfile(script_name):
        print(f"🔹 Running {script_name}...")
        subprocess.run([admet_ai_python, script_name], check=True)
        print(f"✅ {script_name} completed successfully.")
    else:
        print(f"❌ Script '{script_name}' not found.")
        sys.exit(1)

for script in ["admet_v2.py", "ADMET_DataProcess.py"]:
    run_script(script)

# ==== Step 3: Load CSV and prepare PDF ====
csv_path = Path("input_admet_predictions.csv")
image_path = Path("admet_radar_chart.png")
output_pdf = csv_path.with_name("structured_admet_report.pdf")

df = pd.read_csv(csv_path)
df.columns = df.columns.str.strip()
compound_data = df.iloc[0]  # First compound

def resolve_units(prop):
    return {
        "molecular_weight": "Dalton",
        "logp": "log-ratio",
        "tpsa": "A²",
        "ld50_zhu": "log(1/(mol/kg))",
        "clearance_hepatocyte_az": "µL/min/10⁶ cells",
        "clearance_microsome_az": "µL/min/mg",
        "half_life_obach": "hr",
        "ppbr_az": "%",
        "vdss_lombardo": "L/kg",
        "solubility_aqsoldb": "log(mol/L)",
        "lipophilicity_astrazeneca": "log-ratio",
        "caco2_wang": "log(10⁻⁶-cm/s)",
        "hydrationfreeenergy_freesolv": "kcal/mol"
    }.get(prop.lower(), "")

sections = {
    "Physicochemical": ["molecular_weight","logP","hydrogen_bond_acceptors","hydrogen_bond_donors","Lipinski","QED","stereo_centers","tpsa"],
    "Absorption": ["Bioavailability_Ma","PAMPA_NCATS","Pgp_Broccatelli","Caco2_Wang","HydrationFreeEnergy_FreeSolv","Lipophilicity_AstraZeneca","Solubility_AqSolDB"],
    "Distribution": ["BBB_Martins","PPBR_AZ","VDss_Lombardo"],
    "Metabolism": ["CYP1A2_Veith","CYP2C19_Veith","CYP2C9_Substrate_CarbonMangels","CYP2C9_Veith","CYP2D6_Substrate_CarbonMangels","CYP2D6_Veith","CYP3A4_Substrate_CarbonMangels","CYP3A4_Veith"],
    "Excretion": ["Clearance_Hepatocyte_AZ","Clearance_Microsome_AZ","Half_Life_Obach"],
    "Toxicity": ["AMES","QED","Carcinogens_Lagunin","ClinTox","DILI","NR-AR-LBD","NR-AR","NR-AhR","NR-Aromatase","NR-ER-LBD","NR-ER","NR-PPAR-gamma","SR-ARE","SR-ATAD5","SR-HSE","SR-MMP","SR-p53","Skin_Reaction","hERG","LD50_Zhu"]
}

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name="SectionHeader", fontSize=11, leading=11, textColor=colors.whitesmoke, backColor=colors.purple, alignment=1, spaceAfter=3, spaceBefore=6))
styles.add(ParagraphStyle(name="TableBody", fontSize=11, leading=11))

def make_section(title, props):
    data = [["Property","Prediction","DrugBank Percentile","Units"]]
    for prop in props:
        prediction = compound_data.get(prop, "N/A")
        percentile_col = f"{prop}_drugbank_approved_percentile"
        percentile = compound_data.get(percentile_col, "N/A")
        units = resolve_units(prop)
        data.append([prop, prediction, percentile, units])
    table = Table(data, colWidths=[2.5*inch,1.5*inch,1.5*inch,1*inch], repeatRows=1)
    table.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,0),colors.HexColor('#003366')),
        ('TEXTCOLOR',(0,0),(-1,0),colors.whitesmoke),
        ('ALIGN',(0,0),(-1,-1),'LEFT'),
        ('INNERGRID',(0,0),(-1,-1),0.5,colors.grey),
        ('FONTNAME',(0,0),(-1,0),'Helvetica-Bold'),
        ('BACKGROUND',(0,1),(-1,-1),colors.HexColor('#f2f2f2')),
        ('BOX',(0,0),(-1,-1),1,colors.grey)
    ]))
    return Paragraph(title, getSampleStyleSheet()['Heading2']), table

doc = SimpleDocTemplate(str(output_pdf), pagesize=letter)
elements = [Paragraph("ADMET Properties Report", styles['Title']), Spacer(1,6)]

if image_path.exists():
    elements += [Paragraph("Radar Chart Overview", styles['Heading2']),
                 Spacer(1,3),
                 Image(str(image_path), width=5*inch, height=5*inch),
                 Spacer(1,6)]

for sec_title, props in sections.items():
    header, table = make_section(sec_title, props)
    elements.extend([header, Spacer(1,3), table, Spacer(1,6)])

doc.build(elements)
print(f"✅ PDF generated: {output_pdf}")

# ==== Automatically open PDF ====
def open_file(filepath):
    if platform.system() == "Windows":
        os.startfile(filepath)
    elif platform.system() == "Darwin":  # macOS
        subprocess.run(["open", filepath])
    else:
        subprocess.run(["xdg-open", filepath])

open_file(str(output_pdf))

# ==== Step 4 & 5: Run ligand prep and then molecular docking ====
def run_ligand_prep_and_docking():
    ligand_name = input("Enter ligand file name (without .pdb): ").strip()
    charge = input("Enter charge value: ").strip()
    input_log = input("Enter input log file name (with extension, e.g., input.log): ").strip()

    ligand_file = f"{ligand_name}.pdb"
    ligand_opt_file = f"{ligand_name}_opt.pdb"

    # Check files
    if not os.path.isfile(ligand_file):
        print(f"❌ Ligand file '{ligand_file}' not found in current directory.")
        return
    if not os.path.isfile(input_log):
        print(f"❌ Input log file '{input_log}' not found.")
        return

    # Set OBABEL_BIN to your fixed obabel
    obabel_bin = os.path.expanduser("~/Desktop/ligmap/mgltools_1.5.7_MacOS-X/bin/obabel")

    # Pass OBABEL_BIN as environment variable to the shell script
    env = os.environ.copy()
    env["OBABEL_BIN"] = obabel_bin

    # --- Run ligand prep ---
    cmd_prep = ["./ligand_prep.sh", "-l", ligand_file, "-c", charge]
    try:
        print(f"🔹 Running ligand prep: {' '.join(cmd_prep)}")
        subprocess.run(cmd_prep, check=True, env=env)
        print("✅ Ligand preparation completed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"❌ Ligand preparation failed with error code {e.returncode}")
        return

    # --- Run molecular docking using same input_log ---
    if not os.path.isfile(ligand_opt_file):
        print(f"❌ Optimized ligand file '{ligand_opt_file}' not found.")
        return

    cmd_dock = ["./molecular_docking_corrected.sh", "-i", input_log, "-l", ligand_opt_file]
    try:
        print(f"🔹 Running molecular docking: {' '.join(cmd_dock)}")
        subprocess.run(cmd_dock, check=True)
        print("✅ Molecular docking completed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"❌ Molecular docking failed with error code {e.returncode}")

# Call the combined function as the last step
run_ligand_prep_and_docking()

run.py
Displaying run.py.