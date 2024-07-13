import os
import sys
import tensorflow as tf
import jax
import pandas as pd
import json
import matplotlib.pyplot as plt
import numpy as np
import re
import csv
from tqdm import tqdm

from tensorflow.python.ops.array_ops import sequence_mask
from matplotlib.cbook import sanitize_sequence

if jax.local_devices()[0].platform == 'cpu':
  print("WARNING: no GPU detected, will be using CPU")
  DEVICE = "cpu"
else:
  print('Running on GPU')
  DEVICE = "gpu"
  # disable GPU on tensorflow
  # tf.config.set_visible_devices([], 'GPU')

if 'alphafold' not in sys.path:
  sys.path.append('alphafold')
if 'ColabFold/beta' not in sys.path:
  sys.path.append('ColabFold/beta')

import colabfold as cf
import ColabFold.beta.colabfold_alphafold as cf_af

if f"tmp/bin" not in os.environ['PATH']:
  os.environ['PATH'] += f":tmp/bin:tmp/scripts"

IN_COLAB = False
jobname = "Immuno"
homooligomer =  "1:1"
msa_method = "mmseqs2" 
add_custom_msa = False 
msa_format = "fas" 
pair_mode = "unpaired" 
pair_cov = 50 
pair_qid = 20 
num_relax = None
rank_by = "pLDDT" 
use_turbo = True 
max_msa = "256:512" 
max_msa_clusters, max_extra_msa = [int(x) for x in max_msa.split(":")]
show_images = False 
num_models = 1 
use_ptm = True 
num_ensemble = 1 
max_recycles = 3 
is_training = False 
num_samples = 1 
subsample_msa = True

if not use_ptm and rank_by == "pTMscore":
  print("WARNING: models will be ranked by pLDDT, 'use_ptm' is needed to compute pTMscore")
  rank_by = "pLDDT"

# change this for different sequences
# sequences = ['GSHSMRYFFTSVSRPGRGEPRFIAVGYVDDTQFVRFDSDAASQRMEPRAPWIEQEGPEYWDGETRKVKAHSQTHRVDLGTLRGYYNQSEAGSHTVQRMYGCDVGSDWRFLRGYHQYAYDGKDYIALKEDLRSWTAADMAAQTTKHKWEAAHVAEQLRAYLEGTCVEWLRRYLENGKETLQRTDAPKTHMTHHAVSDHEATLRCWALSFYPAEITLTWQRDGEDQTQDTELVETRPAGDGTFQKWAAVVVPSGQEQRYTCHVQHEGLPKPLTLRSVVSTDDDLA:YLANGGFLI']

complex_data_list_pae = []
complex_data_list_contacts = []
complex_data_list_distances = []
complex_data_list_plddt = []

target_csv = "D:\\Edward\\YALE\\CPSC\\552\\immunoai\\data\\hadrup_viral_data_csv.csv"

# 420 samples per job
start = int(sys.argv[1])
end = int(sys.argv[2])
print("Subsection: " +  str(start) + ": " + str(end) )

with open(target_csv, "r") as f:
  reader = csv.reader(f)
  for count, line in enumerate(tqdm(reader)):
    if count==0:
      continue
    count = count - 1

    if count<start or count>end: # skip the samples that aren't part of this job
      continue 

    peptide = line[1] # line[2] for mut_pep
    sequence = line[3]
    sequence = sequence + ":" + peptide

    sequence_length = len(sequence)-1

    I = cf_af.prep_inputs(sequence, jobname + sequence[-100:].replace(":", ""), homooligomer, clean=IN_COLAB)
    mod_I = cf_af.prep_msa(I, msa_method, add_custom_msa, msa_format,
                      pair_mode, pair_cov, pair_qid, TMP_DIR="tmp")

    feature_dict = cf_af.prep_feats(mod_I, clean=IN_COLAB)
    Ls_plot = feature_dict["Ls"]

    # prep model options
    opt = {"N":len(feature_dict["msa"]),
          "L":len(feature_dict["residue_index"]),
          "use_ptm":use_ptm,
          "use_turbo":use_turbo,
          "num_relax" : num_relax,
          "max_recycles": max_recycles,
          "tol":0.0,
          "num_ensemble":num_ensemble,
          "max_msa_clusters":max_msa_clusters,
          "max_extra_msa":max_extra_msa,
          "is_training":is_training}

    if use_turbo:
      if "runner" in dir():
        # only recompile if options changed
        runner = cf_af.prep_model_runner(opt, old_runner=runner)
      else:
        runner = cf_af.prep_model_runner(opt, params_loc='D:\\Edward\\YALE\\CPSC\\552\\immunoai\\alphafold\\alphafold\\data')

    else:
      runner = None

    ###########################
    # run alphafold
    ###########################
    outs, model_rank = cf_af.run_alphafold(feature_dict, opt, runner, num_models, num_samples, subsample_msa,
                                          rank_by=rank_by, show_images=show_images, 
                                          params_loc='D:\\Edward\\YALE\\CPSC\\552\\immunoai\\alphafold\\alphafold\\data')

    rank_dfs_pae = [pd.DataFrame(outs[k]["pae"]) for k in model_rank]
    full_rank_df_pae = pd.concat(rank_dfs_pae)
    full_rank_df_pae['feature'] = 'PAE'
    full_rank_df_pae['model'] = ['rank1']*sequence_length # + ['rank2']*sequence_length + ['rank3']*sequence_length
    full_rank_df_pae['peptide'] = mod_I['seqs'][1]
    
    rank_dfs_contacts = [pd.DataFrame(outs[k]["adj"]) for k in model_rank]
    full_rank_df_contacts = pd.concat(rank_dfs_contacts)
    full_rank_df_contacts['feature'] = 'contacts'
    full_rank_df_contacts['model'] = ['rank1']*sequence_length # + ['rank2']*sequence_length # + ['rank3']*sequence_length
    full_rank_df_contacts['peptide'] = mod_I['seqs'][1]

    rank_dfs_distances = [pd.DataFrame(outs[k]["dists"]) for k in model_rank]
    full_rank_df_distances = pd.concat(rank_dfs_distances)
    full_rank_df_distances['feature'] = 'distances'
    full_rank_df_distances['model'] = ['rank1']*sequence_length # + ['rank2']*sequence_length # + ['rank3']*sequence_length
    full_rank_df_distances['peptide'] = mod_I['seqs'][1]

    rank_dfs_plddt = [pd.DataFrame(outs[k]["plddt"] for k in model_rank)]
    full_rank_df_plddt = pd.concat(rank_dfs_plddt)
    full_rank_df_plddt['feature'] = 'plddt'
    full_rank_df_plddt['model'] = ['rank1'] # + ['rank2'] + ['rank3']
    full_rank_df_plddt['peptide'] = mod_I['seqs'][1]

    complex_data_list_pae.append(full_rank_df_pae)
    complex_data_list_contacts.append(full_rank_df_contacts)
    complex_data_list_distances.append(full_rank_df_distances)
    complex_data_list_plddt.append(full_rank_df_plddt)

    # clear cache by uploading 20 sequences as one dataframe
    if count%20==0 and count!=start:
      master_df_pae = pd.concat(complex_data_list_pae)
      master_df_contacts = pd.concat(complex_data_list_contacts)
      master_df_distances = pd.concat(complex_data_list_distances)
      master_df_plddt = pd.concat(complex_data_list_plddt)

      master_df = pd.concat([master_df_pae,master_df_contacts,master_df_distances, master_df_plddt])
      master_df.to_csv("immuno" + str(count) + '.csv')

      complex_data_list_pae = []
      complex_data_list_contacts = []
      complex_data_list_distances = []
      complex_data_list_plddt = []

      # clear variables as well
      master_df_pae = []
      master_df_contacts = []
      master_df_distances = []
      master_df_plddt = []

    print('next_complex')

  master_df_pae = pd.concat(complex_data_list_pae)
  master_df_contacts = pd.concat(complex_data_list_contacts)
  master_df_distances = pd.concat(complex_data_list_distances)
  master_df_plddt = pd.concat(complex_data_list_plddt)

  master_df = pd.concat([master_df_pae,master_df_contacts,master_df_distances, master_df_plddt])
  master_df.to_csv("immuno" + str(end) + '.csv')