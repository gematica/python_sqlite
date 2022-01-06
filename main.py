import sqlite3
import json

conexion=sqlite3.connect("data.sqlite")
cursor=conexion.execute("select * from notes")
row_headers=[x[0] for x in cursor.description] #this will extract row headers
rv = cursor.fetchall()

json_data=[]
for result in rv:
    dict_from_list = dict(zip(row_headers, result))
#    print(dict_from_list)
    json_data.append(dict_from_list)

a = json.dumps(json_data)
print(a)
conexion.close()