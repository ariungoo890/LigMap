#checking if the smiles is correct
from rdkit import Chem 
smiles = "CC(C)OC(=O)CC(=O)CSc1nc2c(cc1C#N)CCC2"
mol = Chem.MolFromSmiles(smiles)
if mol: 
    print("Valid SMILES")
else:
    print("invalid SMILES")

#If SMILES is INVALID use "pubchem sketcher"
#import chemical structure choose the export as SMILES 
#copy generated SMILES