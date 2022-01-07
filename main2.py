import sqlite3

def row_to_dict(cursor: sqlite3.Cursor, row: sqlite3.Row) -> dict:
    data = {}
    for idx, col in enumerate(cursor.description):
        data[col[0]] = row[idx]
    return data

with sqlite3.connect("data.sqlite") as con:
    con.row_factory = row_to_dict
    result = con.execute('SELECT * FROM notes')
    print(result.fetchall())