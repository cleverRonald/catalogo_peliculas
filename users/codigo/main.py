from flask import Flask, jsonify, request, Response
from flask_pymongo import PyMongo
from bson import json_util
from bson.objectid import ObjectId
import json

from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

app.secret_key = 'masterkey'

app.config['MONGO_URI'] = 'mongodb://192.168.99.100:27017/users'


mongo = PyMongo(app)

## CREATE  USERS  "POST" #############################

@app.route('/users', methods=['POST'])
def create_user():
    # Receiving Data
    firstname = request.json['firstname']
    lastname = request.json['lastname']
    email = request.json['email']
    password = request.json['password']

    if firstname and lastname and email and password:
        hashed_password = generate_password_hash(password)
        id = mongo.db.users.insert(
            {'firstname': firstname,'lastname':lastname, 'email': email, 'password': hashed_password})
        response = jsonify({
            '_id': str(id),
            'firstname': firstname,
            'lastname':lastname,
            'email': email,
            'password': password
        })
        response.status_code = 201
        return response
    else:
        return not_found()

# MOSTRAR USERS  "GET"  ################################

@app.route('/users', methods=['GET'])
def get_users():
    users = mongo.db.users.find()
    response = json_util.dumps(users)
    return Response(response, mimetype="application/json")

# MOSTRAR  {ID} USERS  "GET"  ################################

@app.route('/users/<id>', methods=['GET'])
def get_user(id):
    print(id)
    user = mongo.db.users.find_one({'_id': ObjectId(id), })
    response = json_util.dumps(user)
    return Response(response, mimetype="application/json")

# ELIMINAR  {ID} USERS  "GET"  ################################

@app.route('/users/<id>', methods=['DELETE'])
def delete_user(id):
    mongo.db.users.delete_one({'_id': ObjectId(id)})
    response = jsonify({'message': 'Usuario ' + id + ' eliminado exitosamente'})
    response.status_code = 200
    return response

# UPDATE  {ID} USERS  "GET"  ################################

@app.route('/users/<_id>', methods=['PUT'])
def update_user(_id):
    firstname = request.json['firstname']
    lastname = request.json['lastname']
    email = request.json['email']
    password = request.json['password']
    if firstname and lastname and email and password and _id:
        hashed_password = generate_password_hash(password)
        mongo.db.users.update_one(
            {'_id': ObjectId(_id['$oid']) if '$oid' in _id else ObjectId(_id)}, {'$set': {'firstname': firstname,'lastname':lastname, 'email': email, 'password': hashed_password}})
        response = jsonify({'message': 'Usuario' + _id + ' actualizado exitosamente'})
        response.status_code = 200
        return response
    else:
      return not_found()


@app.errorhandler(404)
def not_found(error=None):
    message = {
        'message': 'Pagina no encontrada ' + request.url,
        'status': 404
    }
    response = jsonify(message)
    response.status_code = 404
    return response


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=4000,debug = True)