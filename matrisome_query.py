# py_cluster_3.matrisomedb_pandas_sql created by bathy at 9/8/2022
import sqlite3
import pandas as pd

connection = sqlite3.connect("matrisome_db3.db")
# df = pd.read_sql_query("SELECT * FROM protein_info LIMIT 50000", connection)
df = pd.read_sql_query("SELECT * FROM protein_info WHERE gene_name ='Col12a1'",connection)
# print(df.iloc[0], df.columns
print (df.shape)
print (df.columns)
# print (df.iloc[10,:])
selected = df[df['sample_type']=='Pancreatic Ductal Adenocarcinoma Xenograft (BxPC3)']
selected.to_csv('F:/matrisomedb2.0/statistics/Col12a1_Pancreatic Ductal Adenocarcinoma Xenograft (BxPC3).tsv',sep='\t')
# for column in df.columns:
#     for each in df[column]:
#         if type(each) == str and each.split(' ')[-1] == '':
#             print (each)
# df = pd.read_sql_query("SELECT DISTINCT sample_type from protein_info", connection)
# print(df)
