# py_cluster_3.matrisomedb_pandas_sql created by bathy at 9/8/2022
import sqlite3
import pandas as pd

connection = sqlite3.connect("matrisome_db.db")
df = pd.read_sql_query("SELECT * FROM protein_info LIMIT 500", connection)
# print(df.iloc[0], df.columns)
print (df.columns)
print (df.iloc[10,:])
# df = pd.read_sql_query("SELECT DISTINCT sample_type from protein_info", connection)
# print(df)
