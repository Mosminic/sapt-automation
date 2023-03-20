from fireworks.utilities.fw_utilities import explicit_serialize
from fireworks.core.firework import FiretaskBase, FWAction
import psi4
import pandas as pd
import re
from pymongo import MongoClient

def generate_geometry(xyz_string):
    mols = xyz_string.split("\n")
    mols = mols[2:]

    geometry = "0 1\n"
    for idx in range(int(len(mols) / 2)):
        if mols[idx] != "":
            geometry += mols[idx] + "\n"

    geometry += "--\n0 1\n"
    for idx in range(int(len(mols) / 2), len(mols)):
        if mols[idx] != "":
            geometry += mols[idx] + "\n"

    return geometry


@explicit_serialize
class SAPT(FiretaskBase):

    def run_task(self, fw_spec):
        # read the XYZ file
        dimerName = self["xyz"]
        # sapt calculations
        psi4.core.set_output_file('dimer.out', False)
        psi4.set_num_threads(48)
        psi4.set_memory("170 GB")
        psi4.core.IOManager.shared_object().set_default_path('.')
        dimer = psi4.geometry(generate_geometry(dimerName))
    
        psi4.set_options({'scf_type': 'df', 'freeze_core': 'true'})
    
        psi4.energy('sapt0/jun-cc-pvdz', molecule=dimer)
    
        # create the SAPT input        
        outfilename = "dimer.out"
        with open(outfilename,"r") as f:
            lines = f.readlines()

        # patterns to look up
        start_pattern = re.compile(r'SAPT Results')
        end_pattern = re.compile(r'Special recipe for scaled SAPT0')
        float_patt = re.compile(r"\s*([+-]?\d+\.\d+)")
        string_patt = re.compile(r'^[A-Z]*')


        # find line with start pattern
        for idx, line in enumerate(lines): # loops over the lines
            if re.match(start_pattern,line.strip()):
                break
        print("Start pattern found at line",idx+1)


        # parse lines
        idx = idx + 2
        line = lines[idx]

        parsed_lines = []
        while not(re.match(end_pattern,line.strip())):
            parsed_lines.append(line.strip())
            idx += 1
            line = lines[idx]

        # set line numbers for energies to extract from parsed lines
        line_info = [("Electrostatics", 0), ("Exchange", 3), ("Induction", 7), ("Dispersion", 12), ("Total", 21)]
        
        # extract data from lines
        data = {}
        data.update({"label":self["label"]})
        data.update({"identifier":self["identifier"]})
        data.update({"xyz": self["xyz"]})
        for energy, number in line_info:
            value = round(float(float_patt.findall(parsed_lines[number])[1]),2)
            data.update({energy:value})
        
        # parse the results to a database    
        client = MongoClient("mongodb://10.33.30.11:23771/fair_test1?retryWrites=false")
        db = client["fair_test1"]
        collection = db["results"]
        collection.update_one({"_id": self["identifier"] + self["label"]}, {"$set": data}, upsert=True)
