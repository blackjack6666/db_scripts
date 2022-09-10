import sqlite3
import glob
import os
import pandas as pd
result_dir = r'F:/matrisomedb2.0/MDB2/result/'
result_files = glob.glob(os.path.join(result_dir, "**/*_summary.tsv"), recursive=True)
con = sqlite3.connect("matrisome_db4.db")
cur = con.cursor()
# no need to modify this line
cur.execute("CREATE TABLE IF NOT EXISTS protein_info (ID INTEGER PRIMARY KEY AUTOINCREMENT, uniprot_id CHAR, gene_name CHAR, species CHAR, category CHAR, tissue CHAR, organ_system CHAR, tissue_class CHAR, sample_type CHAR, data_source CHAR, repository_id CHAR, matrisome_category CHAR, matrisome_class CHAR, file_name CHAR, reference CHAR, description CHAR, note CHAR, total_psm INT, hyperscore_sum DOUBLE, seq_cov_file CHAR, NSAF DOUBLE);")
j = 0
for each in result_files:
    j += 1
    if j % 100 == 0:
        print(j, each)
    df = pd.read_csv(each, sep='\t')
    df = df.drop(columns = ['Unnamed: 0', 'note'])
    data = df.values.tolist()
    cur.executemany("""insert into protein_info(uniprot_id, gene_name, species, tissue, organ_system, sample_type, repository_id, matrisome_category, matrisome_class, file_name, reference, description, total_psm, hyperscore_sum, NSAF, seq_cov_file ) values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);""",
                    data)
cur.execute("""CREATE INDEX "" ON protein_info (gene_name ASC, species, sample_type, matrisome_class, matrisome_category, description)""")
con.commit()
cur.close()