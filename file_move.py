import shutil
import os
from glob import glob
import pickle

# all_txt_file = 'F:/matrisomedb2.0/output_all.txt'
# file_list = []
# with open(all_txt_file,'r') as f_o:
#     for line in f_o:
#         file_list.append(line.split('./')[1].split('.html')[0]+'_ptmtable.html')
# file_set = set(file_list)
# # for f in file_list:
# #     shutil.move(r'F:/matrisomedb2.0/table_htmls_2/'+f,r'F:/matrisomedb2.0/ptm_table_html_clean/'+f)
#
# files = glob('F:/matrisomedb2.0/table_htmls_2/*.html')
#
# for each in files:
#     file_name = each.split('\\')[-1]
#     file_name_clean = file_name.replace("\xa0"," ")
#     if file_name_clean in file_set:
#         shutil.move(r'F:/matrisomedb2.0/table_htmls_2/'+file_name, r'F:/matrisomedb2.0/ptm_table_html_clean/'+file_name_clean)

def protein_id_to_species(fasta_file_path):
    with open(fasta_file_path, 'r') as file_open:
        file_split = file_open.read().split('\n>')

    return {each.split('\n')[0].split('|')[1]:each.split('\n')[0].split('OS=')[1].split(' OX=')[0]
            for each in file_split}

protein_species_dict = protein_id_to_species('F:/matrisomedb2.0/mat.fasta')
# print (protein_species_dict)
id_freq_array_dict = pickle.load(open('F:/matrisomedb2.0/glob_prot_freq_dict.p','rb'))
for prot in id_freq_array_dict:
    species = protein_species_dict[prot]
    if species == 'Homo sapiens':
        alphafold_path = 'D:/data/alphafold_pdb/UP000005640_9606_HUMAN/AF-'+prot+'-F1-model_v1.pdb'
    elif species == 'Mus musculus':
        alphafold_path = 'D:/data/alphafold_pdb/UP000000589_10090_MOUSE/AF-' + prot + '-F1-model_v1.pdb'
    try:
        shutil.copy(alphafold_path,'F:/matrisomedb2.0/mat_alphafold_pdbs/')
    except:
        continue