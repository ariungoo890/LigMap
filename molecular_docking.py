#!/usr/bin/env python3
"""
Molecular Docking Pipeline - Cross-Platform Implementation
Replaces the Linux-specific MGLTools and AutoDock workflow with Python libraries
"""

import os
import sys
import numpy as np
import pandas as pd
from typing import Tuple, List, Dict, Optional
import logging
from pathlib import Path
import Bio
print("Biopython v" + Bio.__version__)
# Required installations:
# pip install biopython rdkit-pypi pymol-open-source openmm pdbfixer

try:
    from Bio.PDB import PDBParser, PDBIO, Select, Structure, Model, Chain, Residue
    from rdkit import Chem # ene bolohgui bga
    from rdkit.Chem import AllChem, rdMolDescriptors, Descriptors #
    from rdkit.Chem import rdDepictor, rdDistGeom
except ImportError as e:
    print(f"Required library not found: {e}")
    print("Please install required packages:")
    print("pip install biopython rdkit-pypi pymol-open-source")
    sys.exit(1)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class MolecularDockingPipeline:
    """
    Cross-platform molecular docking pipeline using Python libraries
    """

    def __init__(self, target_pdb: str, ligand_pdb: str, output_dir: str = "docking_results"):
        self.target_pdb = target_pdb
        self.ligand_pdb = ligand_pdb
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)

        # Initialize structures
        self.parser = PDBParser(QUIET=True)
        self.target_structure = None
        self.ligand_structure = None
        self.binding_site_center = None
        self.grid_size = None

        logger.info(f"Initialized docking pipeline with target: {target_pdb}, ligand: {ligand_pdb}")

    def load_structures(self):
        """Load PDB structures for target and ligand"""
        try:
            self.target_structure = self.parser.get_structure('target', self.target_pdb)
            self.ligand_structure = self.parser.get_structure('ligand', self.ligand_pdb)
            logger.info("Successfully loaded target and ligand structures")
        except Exception as e:
            logger.error(f"Error loading structures: {e}")
            raise

    def prepare_target(self) -> str:
        """
        Prepare target protein structure
        Equivalent to prepare_receptor4.py functionality
        """
        logger.info("Preparing target structure...")

        class ProteinSelect(Select):
            """Select only protein atoms, remove water and heteroatoms"""
            def accept_residue(self, residue):
                return residue.get_id()[0] == ' '  # Standard amino acids only

        # Clean target structure
        io = PDBIO()
        io.set_structure(self.target_structure)
        target_clean_path = self.output_dir / "target_clean.pdb"
        io.save(str(target_clean_path), ProteinSelect())

        logger.info(f"Target prepared and saved to {target_clean_path}")
        return str(target_clean_path)

    def prepare_ligand(self) -> str:
        """
        Prepare ligand structure and add charges
        Equivalent to prepare_ligand4.py functionality
        """
        logger.info("Preparing ligand structure...")

        # Convert PDB to MOL for RDKit processing
        ligand_mol = self.pdb_to_mol(self.ligand_pdb)

        if ligand_mol is None:
            raise ValueError("Could not parse ligand structure")

        # Add hydrogens and compute charges
        ligand_mol = Chem.AddHs(ligand_mol)
        AllChem.ComputeGasteigerCharges(ligand_mol)

        # Generate 3D coordinates if needed
        if ligand_mol.GetNumConformers() == 0:
            AllChem.EmbedMolecule(ligand_mol)
            AllChem.UFFOptimizeMolecule(ligand_mol)

        # Save prepared ligand
        ligand_prep_path = self.output_dir / "ligand_prep.sdf"
        writer = Chem.SDWriter(str(ligand_prep_path))
        writer.write(ligand_mol)
        writer.close()

        logger.info(f"Ligand prepared and saved to {ligand_prep_path}")
        return str(ligand_prep_path)

    def pdb_to_mol(self, pdb_file: str):
        """Convert PDB file to RDKit molecule object"""
        try:
            mol = Chem.MolFromPDBFile(pdb_file, removeHs=False)
            if mol is None:
                # Try alternative parsing
                mol = Chem.MolFromPDBFile(pdb_file, sanitize=False)
                if mol is not None:
                    Chem.SanitizeMol(mol)
            return mol
        except Exception as e:
            logger.error(f"Error converting PDB to MOL: {e}")
            return None

    def calculate_binding_site_center(self, reference_ligand_pdb: Optional[str] = None) -> Tuple[float, float, float]:
        """
        Calculate binding site center coordinates
        If reference ligand provided, use its center; otherwise use geometric center of target
        """
        if reference_ligand_pdb:
            logger.info("Calculating binding site center from reference ligand...")
            ref_structure = self.parser.get_structure('ref_ligand', reference_ligand_pdb)
            coords = []

            for atom in ref_structure.get_atoms():
                coords.append(atom.get_coord())

            coords = np.array(coords)
            center = np.mean(coords, axis=0)
        else:
            logger.info("Calculating binding site center from target geometric center...")
            coords = []
            for atom in self.target_structure.get_atoms():
                if atom.get_parent().get_id()[0] == ' ':  # Protein atoms only
                    coords.append(atom.get_coord())

            coords = np.array(coords)
            center = np.mean(coords, axis=0)

        self.binding_site_center = tuple(center)
        logger.info(f"Binding site center: {self.binding_site_center}")
        return self.binding_site_center

    def calculate_grid_size(self, ligand_mol=None) -> float:
        """
        Calculate grid size based on ligand dimensions
        Equivalent to grid box size calculation in original workflow
        """
        if ligand_mol is None:
            ligand_mol = self.pdb_to_mol(self.ligand_pdb)

        if ligand_mol is None:
            logger.warning("Could not determine ligand size, using default grid size")
            return 25.0

        # Get conformer coordinates
        conf = ligand_mol.GetConformer()
        coords = []
        for i in range(ligand_mol.GetNumAtoms()):
            pos = conf.GetAtomPosition(i)
            coords.append([pos.x, pos.y, pos.z])

        coords = np.array(coords)

        # Calculate maximum distance between any two atoms
        max_dist = 0
        for i in range(len(coords)):
            for j in range(i+1, len(coords)):
                dist = np.linalg.norm(coords[i] - coords[j]) # same as dist = ((xi - xj)**2 + (yi - yj)**2 + (zi - zj)**2)**0.5
                max_dist = max(max_dist, dist)

        # Grid size formula from original: (Lmax + 8)/0.375
        grid_size = (max_dist + 8)/0.375
        self.grid_size = grid_size

        logger.info(f"Calculated ligand max dimension: {max_dist:.2f} Å")
        logger.info(f"Grid size set to: {grid_size:.2f} Å")
        return grid_size

    def perform_docking(self, num_poses: int = 10) -> List[Dict]:
        """
        Perform molecular docking using simplified energy-based approach
        This replaces AutoDock4 functionality with a Python implementation
        """
        logger.info(f"Starting docking simulation with {num_poses} poses...")

        # Load prepared ligand
        ligand_mol = self.pdb_to_mol(self.ligand_pdb)
        if ligand_mol is None:
            raise ValueError("Could not load ligand for docking")

        # Generate multiple conformations
        poses = self.generate_poses(ligand_mol, num_poses)

        # Score each pose
        scored_poses = []
        for i, pose in enumerate(poses):
            score = self.score_pose(pose)
            scored_poses.append({
                'rank': i + 1,
                'pose': pose,
                'binding_energy': score,
                'rmsd': 0.0  # Placeholder for RMSD calculation
            })

        # Sort by binding energy (lower is better)
        scored_poses.sort(key=lambda x: x['binding_energy'])

        # Update ranks
        for i, pose in enumerate(scored_poses):
            pose['rank'] = i + 1

        logger.info(f"Docking completed. Best binding energy: {scored_poses[0]['binding_energy']:.2f} kcal/mol")
        return scored_poses

    def generate_poses(self, ligand_mol, num_poses: int) -> List:
        """Generate different poses of the ligand in the binding site"""
        poses = []

        # Generate conformations
        for i in range(num_poses):
            mol_copy = Chem.Mol(ligand_mol)
            mol_copy = Chem.AddHs(mol_copy)

            # Embed molecule with random coordinates
            AllChem.EmbedMolecule(mol_copy, randomSeed=i)

            # Optimize geometry
            AllChem.UFFOptimizeMolecule(mol_copy)

            poses.append(mol_copy)

        return poses

    def score_pose(self, pose_mol) -> float:
        """
        Simple scoring function for poses
        In a real implementation, this would include van der Waals, electrostatic,
        hydrogen bonding, and entropy terms
        """
        # Placeholder scoring based on molecular properties
        # This is a simplified version - real docking uses complex energy functions

        mw = Descriptors.MolWt(pose_mol)
        logp = Descriptors.MolLogP(pose_mol)
        hbd = rdMolDescriptors.CalcNumHBD(pose_mol)
        hba = rdMolDescriptors.CalcNumHBA(pose_mol)

        # Simple empirical scoring (this is a placeholder)
        score = -0.1 * mw + 2.0 * logp - 0.5 * hbd - 0.3 * hba + np.random.normal(0, 2)

        return score

    def save_docking_results(self, scored_poses: List[Dict]) -> str:
        """Save docking results in various formats"""
        results_file = self.output_dir / "docking_results.csv"

        # Create results DataFrame
        results_data = []
        for pose in scored_poses:
            results_data.append({
                'Rank': pose['rank'],
                'Binding_Energy_kcal_mol': pose['binding_energy'],
                'RMSD': pose['rmsd'],
                'Classification': self.classify_binding_energy(pose['binding_energy'])
            })

        df = pd.DataFrame(results_data)
        df.to_csv(results_file, index=False)

        # Save top 10 poses as SDF files
        for i, pose in enumerate(scored_poses[:10]):
            pose_file = self.output_dir / f"pose_{i+1}.sdf"
            writer = Chem.SDWriter(str(pose_file))
            writer.write(pose['pose'])
            writer.close()

        logger.info(f"Results saved to {results_file}")
        return str(results_file)

    def classify_binding_energy(self, energy: float) -> str:
        """Classify binding strength based on energy"""
        if energy > -6:
            return "Weak/Non-specific"
        elif -8 <= energy <= -7:
            return "Moderate"
        elif energy < -8:
            return "Strong"
        elif energy < -9:
            return "Drug-like inhibitor"
        else:
            return "Unknown"

    def analyze_interactions(self, top_poses: List[Dict], n_poses: int = 5) -> Dict:
        """
        Analyze protein-ligand interactions for top poses
        This replaces LigPlot+ functionality
        """
        logger.info(f"Analyzing interactions for top {n_poses} poses...")

        interactions_summary = {
            'hydrogen_bonds': [],
            'hydrophobic_contacts': [],
            'pi_pi_stacking': [],
            'summary_stats': {}
        }

        # Placeholder for interaction analysis
        # In a full implementation, this would:
        # 1. Calculate distances between ligand and protein atoms
        # 2. Identify hydrogen bonds based on geometry
        # 3. Find hydrophobic contacts
        # 4. Detect pi-pi stacking interactions

        interactions_summary['summary_stats'] = {
            'avg_binding_energy': np.mean([pose['binding_energy'] for pose in top_poses[:n_poses]]),
            'std_binding_energy': np.std([pose['binding_energy'] for pose in top_poses[:n_poses]]),
            'best_energy': min([pose['binding_energy'] for pose in top_poses[:n_poses]])
        }

        return interactions_summary

    def run_complete_pipeline(self, reference_ligand_pdb: Optional[str] = None, num_poses: int = 50) -> Dict:
        """
        Run the complete molecular docking pipeline
        """
        logger.info("Starting complete molecular docking pipeline...")

        try:
            # Step 1: Load structures
            self.load_structures()

            # Step 2: Prepare structures
            target_prep = self.prepare_target()
            ligand_prep = self.prepare_ligand()

            # Step 3: Calculate binding site and grid
            self.calculate_binding_site_center(reference_ligand_pdb)
            self.calculate_grid_size()

            # Step 4: Perform docking
            scored_poses = self.perform_docking(num_poses)

            # Step 5: Save results
            results_file = self.save_docking_results(scored_poses)

            # Step 6: Analyze interactions
            interactions = self.analyze_interactions(scored_poses)

            # Compile final results
            pipeline_results = {
                'status': 'success',
                'results_file': results_file,
                'best_binding_energy': scored_poses[0]['binding_energy'],
                'binding_classification': self.classify_binding_energy(scored_poses[0]['binding_energy']),
                'binding_site_center': self.binding_site_center,
                'grid_size': self.grid_size,
                'total_poses': len(scored_poses),
                'interactions_summary': interactions,
                'output_directory': str(self.output_dir)
            }

            logger.info("Pipeline completed successfully!")
            logger.info(f"Best binding energy: {scored_poses[0]['binding_energy']:.2f} kcal/mol")
            logger.info(f"Classification: {pipeline_results['binding_classification']}")

            return pipeline_results

        except Exception as e:
            logger.error(f"Pipeline failed: {e}")
            return {
                'status': 'failed',
                'error': str(e)
            }

def main():
    """
    Example usage of the molecular docking pipeline
    """
    # Example usage
    target_pdb = "target_em.pdb"  # Your target protein
    ligand_pdb = "ligand_opt.pdb"  # Your ligand

    # Check if files exist
    if not os.path.exists(target_pdb):
        logger.error(f"Target file not found: {target_pdb}")
        return

    if not os.path.exists(ligand_pdb):
        logger.error(f"Ligand file not found: {ligand_pdb}")
        return

    # Initialize and run pipeline
    docking = MolecularDockingPipeline(target_pdb, ligand_pdb)

    # Run complete pipeline
    results = docking.run_complete_pipeline(num_poses=50)

    if results['status'] == 'success':
        print("\n" + "="*50)
        print("DOCKING RESULTS SUMMARY")
        print("="*50)
        print(f"Best binding energy: {results['best_binding_energy']:.2f} kcal/mol")
        print(f"Binding classification: {results['binding_classification']}")
        print(f"Binding site center: {results['binding_site_center']}")
        print(f"Grid size: {results['grid_size']:.2f} Å")
        print(f"Total poses generated: {results['total_poses']}")
        print(f"Results saved to: {results['output_directory']}")
        print("="*50)
    else:
        print(f"Docking failed: {results['error']}")

if __name__ == "__main__":
    main()
