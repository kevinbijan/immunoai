import pickle 
import os 
import csv
import subprocess
from tqdm import tqdm

rootdir = 'D:\\Edward\\YALE\\CPSC\\552\\immunoai' # \\prediction_Immunogenicity_080f2\\msa.pickle

target_csv = "D:\\Edward\\YALE\\CPSC\\552\\immunoai\\data\\hadrup_viral_data_csv.csv"

target_folder = 'D:\\Edward\\YALE\\CPSC\\552\\predictions_3'

folds = set()
with open(target_csv, "r") as f:
  reader = csv.reader(f)
  for count, line in enumerate(reader):
    if count==0:
      continue
    peptide = line[1] # line[2] for mut_pep
    sequence = line[3]
    sequence = sequence + peptide
    if sequence in folds: 
       print(sequence)
    folds.add(sequence)

mapping = {}
checked = set()
directories = os.walk(rootdir)
for d in tqdm(directories):
    if "prediction_Immuno" in d[0]:
        if "msa.pickle" not in d[2]:
            print(d[0])
            continue
        with open(d[0]+"\\msa.pickle", 'rb') as f:
            a = pickle.load(f)
        fold = a['msas'][-1][0]
        if fold in folds:
            shortname = d[0].split("\\")[-1]
            bashCommand = "copy " + os.path.join(d[0], "rank_1_model_1_ptm_seed_0_unrelaxed.pdb") + " " + os.path.join(target_folder, "rank_1_" + shortname + ".pdb")
            process = subprocess.run(bashCommand.split(" "), shell=True) 
            # bashCommand = "cp " + d[0] + "\\rank_1_model_1_ptm_seed_0_unrelaxed.pdb " + target_folder + "\\rank_1_" + shortname + ".pdb"
            # process = subprocess.run(bashCommand.split(" ")) 
            # bashCommand = "cp " + d[0] + "\\rank_1_model_2_ptm_seed_0_unrelaxed.pdb " + target_folder + "\\rank_1_" + shortname + ".pdb"
            # process = subprocess.run(bashCommand.split(" ")) 
            # bashCommand = "cp " + d[0] + "\\rank_2_model_2_ptm_seed_0_unrelaxed.pdb " + target_folder + "\\rank_2_" + shortname + ".pdb"
            # process = subprocess.run(bashCommand.split(" ")) 
            # bashCommand = "cp " + d[0] + "\\rank_2_model_1_ptm_seed_0_unrelaxed.pdb " + target_folder + "\\rank_2_" + shortname + ".pdb"
            # process = subprocess.run(bashCommand.split(" ")) 
            mapping[fold] = shortname
            checked.add(fold)

with open(target_folder + '\\mapping.pickle', 'wb') as handle:
    pickle.dump(mapping, handle, protocol=pickle.HIGHEST_PROTOCOL)
print(folds.difference(checked))
# print(mapping)