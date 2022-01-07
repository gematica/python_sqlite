from flask import Flask, jsonify, request
import sqlite3
import json

app = Flask(__name__)

from notes import notes

# Testing Route
@app.route('/ping', methods=['GET'])
def ping():
    return jsonify({'response': 'pong!'})

# Testing Route
@app.route('/', methods=['GET'])
def home():
    return '<h1>Hola Mundo!!!</h1>'

# Get Data Routes
@app.route('/notes')
def getnotes():
    conexion=sqlite3.connect("data.sqlite")
    cursor=conexion.execute("select * from notes")
    row_headers=[x[0] for x in cursor.description] #this will extract row headers
    rv = cursor.fetchall()

    json_data=[]
    for result in rv:
        dict_from_list = dict(zip(row_headers, result))
        json_data.append(dict_from_list)

    #a = json.dumps(json_data)
    conexion.close()
    return jsonify(json_data)
    #return jsonify({'notes': a})
    #return a


@app.route('/notes/<string:id>')
def getNote(id):
    conexion=sqlite3.connect("data.sqlite")
    cursor=conexion.execute("select * from notes where id=" + id)
    row_headers=[x[0] for x in cursor.description] #this will extract row headers
    rv = cursor.fetchall()

    json_data=[]
    for result in rv:
        dict_from_list = dict(zip(row_headers, result))
        json_data.append(dict_from_list)

    #a = json.dumps(json_data)
    conexion.close()
    return jsonify(json_data)
    #return jsonify({'notes': a})
    #return a

# Create Data Routes
@app.route('/notes', methods=['POST'])
def addNote():
    new_note = {
        'name': request.json['name'],
        'price': request.json['price'],
        'quantity': 10
    }
    notes.append(new_note)
    return jsonify({'notes': notes})

# Update Data Route
@app.route('/notes/<string:note_name>', methods=['PUT'])
def editNote(note_name):
    notesFound = [note for note in notes if note['name'] == note_name]
    if (len(notesFound) > 0):
        notesFound[0]['name'] = request.json['name']
        notesFound[0]['price'] = request.json['price']
        notesFound[0]['quantity'] = request.json['quantity']
        return jsonify({
            'message': 'Note Updated',
            'note': notesFound[0]
        })
    return jsonify({'message': 'Note Not found'})

# DELETE Data Route
@app.route('/notes/<string:note_name>', methods=['DELETE'])
def deleteNote(note_name):
    notesFound = [note for note in notes if note['name'] == note_name]
    if len(notesFound) > 0:
        notes.remove(notesFound[0])
        return jsonify({
            'message': 'Note Deleted',
            'notes': notes
        })

if __name__ == '__main__':
    app.run(debug=True, port=4000)
