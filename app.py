from flask import Flask, request, jsonify, Response
from flask_pymongo import PyMongo # Necesita el paquete Flask-PyMongo
from werkzeug.security import generate_password_hash, check_password_hash
from bson import json_util
from bson.objectid import ObjectId
from datetime import datetime
app = Flask(__name__)
# Para conexiones en la nube se requiere tener instalado el paquete dnspython
# También se requiere instalar el paquete pymongo[srv]
app.config["MONGO_URI"] ='mongodb+srv://aarongarcia1906:7300VILLA@cluster0.1qnwzwb.mongodb.net/basemongogym'
mongo = PyMongo(app)

@app.route('/users', methods=['GET'])
def get_users():
    usuarios = mongo.db.users.find()
    response = json_util.dumps(usuarios) # Strings con formato JSON
    return Response(response, mimetype='application/json') # Formato JSON

@app.route('/users', methods=['POST'])
def create_user():
    try:
        request_data = request.get_json()
        if 'username' in request_data and 'name' in request_data and 'password' in request_data and 'weight' in request_data:
            username = request_data['username']
            name = request_data['name']
            password = request_data['password']
            weight = request_data['weight']
            date = request_data.get('date', None)

            hashed_password = generate_password_hash(password)

            user_data = {
                'username': username,
                'name': name,
                'password': hashed_password,
                'weight': weight,
                'date': date
            }

            id = mongo.db.users.insert_one(user_data)

            response = {
                'id': str(id),
                'username': username,
                'name': name,
                'password': hashed_password,
                'weight': weight,
                'date': date
            }

            return jsonify(response)
        else:
            return datos_incompletos()
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    

@app.route('/users/<id>', methods=['GET'])
def get_user_by_id(id):
    try:
        usuario = mongo.db.users.find_one({'_id': ObjectId(id)})
        if usuario:
            response = {
                'id': str(usuario['_id']),
                'username': usuario['username'],
                'name': usuario['name'],
                'password': usuario['password'],
                'weight': usuario['weight'],
                'date': usuario['date']
            }
            return jsonify(response)
        else:
            return not_found()
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/users/<id>', methods=['DELETE'])
def delete_user(id):
    try:
        usuario = mongo.db.users.find_one({'_id': ObjectId(id)})
        if usuario:
            usuarioborrar = mongo.db.users.delete_one({'_id': ObjectId(id)})
            response = jsonify({'mensaje': 'Usuario ' + id + ' fue eliminado satisfactoriamente'})
            return response
        else:
            return not_found()
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.errorhandler(404)
def not_found(error=None):
    response = jsonify({
'mensaje': 'Recurso no encontrado: ' + request.url,
'status': 404
})
    response.status_code = 404
    return response

@app.route('/users/<id>', methods=['PUT'])
def update_user(id):
    try:
        request_data = request.get_json()
        if 'username' in request_data and 'name' in request_data and 'password' in request_data and 'weight' in request_data:
            username = request_data['username']
            name = request_data['name']
            password = request_data['password']
            weight = request_data['weight']
            date = request_data.get('date', None)

            hashed_password = generate_password_hash(password)

            usuario = mongo.db.users.find_one({'_id': ObjectId(id)})
            if usuario:
                mongo.db.users.update_one({'_id': ObjectId(id)}, {'$set':
                {
                    'username': username,
                    'name': name,
                    'password': hashed_password,
                    'weight': weight,
                    'date': date
                }})
            else:
                return not_found()

            response = jsonify({'mensaje': 'Usuario ' + id + ' fue actualizado satisfactoriamente'})
            return response
        else:
            return datos_incompletos()
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.errorhandler(404)
def not_found(error=None):
    response = jsonify({
    'mensaje': 'Recurso no encontrado: ' + request.url,
    'status': 404
    })
    response.status_code = 404
    return response

@app.errorhandler(400)
def datos_incompletos(error=None):
    response = jsonify({
'mensaje': 'Datos incompletos: username, name, password, weight y/o date',
'status': 400
})
    response.status_code = 400
    return response

if __name__ == "__main__":
    app.run(debug=True)