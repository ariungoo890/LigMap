
from admet_ai import ADMETModel

# Define your list of SMILES strings
smiles_list = ["OC1=CC=C(\C=C\C2=C3C(C(OC3=CC3=C2C(C(O3)C2=CC=C(O)C=C2)C2=CC(O)=CC(O)=C2)C2=CC=C(O)C=C2)C2=CC(O)=CC(O)=C2)C=C1"]

# Initialize the model (this is where the logs you saw are generated)
model = ADMETModel()

# Make the predictions and store the result in a variable
predictions_df = model.predict(smiles=smiles_list)
from admet_ai import ADMETModel

model = ADMETModel()
preds = model.predict(smiles="OC1=CC=C(\C=C\C2=C3C(C(OC3=CC3=C2C(C(O3)C2=CC=C(O)C=C2)C2=CC(O)=CC(O)=C2)C2=CC=C(O)C=C2)C2=CC(O)=CC(O)=C2)C=C1")

print(predictions_df)

#Save the DataFrame to a CSV file

predictions_df.to_csv('admet_predicts.csv', index=False)
