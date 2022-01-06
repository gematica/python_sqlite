import sqlite3

conexion=sqlite3.connect("data.sqlite")
cursor=conexion.execute("select * from notes")
for fila in cursor:
    print(fila)
conexion.close()