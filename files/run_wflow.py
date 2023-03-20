from workflow.wflow import *
from fireworks import LaunchPad
import pandas as pd


# Generate the workflow
# change the location of the file each time

csv_location = "/scratch/vka247/sapt_automation/files/ocelot_dimer_v2_sapt.csv"

counter = 0

df = pd.read_csv(csv_location)
for idx, row in df.iterrows():
    if(counter == 0):
        counter = counter + 1
    else:
        wf = SAPTWorkflow(row["identifier"], row["xyz"], row["label"])
        lpad = LaunchPad.from_file("my_launchpad.yaml")
        lpad.add_wf(wf)