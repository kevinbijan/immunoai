import pickle 
import os 
import csv
import subprocess
from tqdm import tqdm

rootdir = '/edward-slow-vol/CPSC_552' # /prediction_Immunogenicity_080f2/msa.pickle

HLA = "/edward-slow-vol/CPSC_552/immunoai/data/HLA_27_seqs.txt"
pep = "/edward-slow-vol/CPSC_552/immunoai/data/immuno_data_multi_allele_for_Edward.txt"

target_folder = '/edward-slow-vol/CPSC_552/alpha_multi/alpha_structure'

HLA_processed = {}
with open(HLA, 'r') as f:
    for count, line in enumerate(f):
        if count == 0:
            continue 
        allele, seq = line.strip().split("\t")
        HLA_processed[allele] = seq

peptides = set()
with open(pep, 'r') as f:
    for count, line in enumerate(f):
        if count == 0:
            continue 
        pep, allele, _ = line.strip().split("\t")
        peptides.add(HLA_processed[allele]+pep)

print(len(peptides))

mapping = {}
checked = set()
directories = os.walk(rootdir)
for d in tqdm(directories):
    if "prediction_Immuno" in d[0]:
        if "msa.pickle" not in d[2]:
            print(d[0])
            continue
        with open(d[0]+"/msa.pickle", 'rb') as f:
            a = pickle.load(f)
        fold = a['msas'][-1][0]
        if fold in peptides:
            shortname = d[0].split("/")[-1]
            bashCommand = "cp " + d[0] + "/rank_1_model_1_ptm_seed_0_unrelaxed.pdb " + target_folder + "/rank_1_" + shortname + ".pdb"
            process = subprocess.run(bashCommand.split(" ")) 
            mapping[fold] = shortname
            checked.add(fold)

with open(target_folder + '/mapping.pickle', 'wb') as handle:
    pickle.dump(mapping, handle, protocol=pickle.HIGHEST_PROTOCOL)
print(peptides.difference(checked))
# print(mapping)