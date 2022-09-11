import pickle
import json
from raw_data_process import protein_info_from_fasta
import numpy as np
import pandas as pd

## sequence coverage
matrix_info_dict = json.load(open('F:/matrisomedb2.0/annotation/mat_dict.json'))
protein_info_dict = protein_info_from_fasta('F:/matrisomedb2.0/mat.fasta')

global_prot_freq_dict = pickle.load(open('F:/matrisomedb2.0/glob_prot_freq_dict.p','rb'))

df = pd.DataFrame(index=[k for k in global_prot_freq_dict.keys()],columns=['Gene','Species','Category','Sub','Sequence coverage'])
for prot in global_prot_freq_dict:
    print (prot)
    gene = protein_info_dict[prot][0]
    species, cate, sub_cate = matrix_info_dict[gene]["Species"], matrix_info_dict[gene]["Category"],matrix_info_dict[gene]["Sub"]
    freq_array = global_prot_freq_dict[prot]
    seq_cov = np.count_nonzero(freq_array)/len(freq_array)*100
    df.loc[prot,'Gene'] = gene
    df.loc[prot,'Species'] = species
    df.loc[prot, 'Category'] = cate
    df.loc[prot, 'Sub'] = sub_cate
    df.loc[prot, 'Sequence coverage'] = seq_cov
df.to_csv('F:/matrisomedb2.0/statistics/glob_seq_coverage.tsv', sep='\t')
