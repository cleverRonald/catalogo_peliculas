from flask import Flask, jsonify, request, Response
from flask_pymongo import PyMongo
from bson import json_util
from bson.objectid import ObjectId
import json
import datetime


app = Flask(__name__)

app.secret_key = 'masterkey'

app.config['MONGO_URI'] = 'mongodb://192.168.99.100:27017/movies'


mongo = PyMongo(app)

## CREATE  movies  "POST" #############################

@app.route('/movies', methods=['POST'])
def create_movies():
    # Receiving Data

    title = request.json['title']
    valoracion = request.json['valoracion']
    descripcion = request.json['descripcion']
    creation =  request.json['creation']


    if title and valoracion and descripcion and creation:
        id = mongo.db.movies.insert(
            {'title': title,'valoracion':valoracion, 'descripcion': descripcion, 'creation': creation})
        response = jsonify({
            '_id': str(id),
            'title': title,
            'valoracion':valoracion,
            'descripcion': descripcion,
            'creation': creation
        })
        response.status_code = 201
        return response
    else:
        return not_found()

# MOSTRAR movies  "GET"  ################################

@app.route('/movies', methods=['GET'])
def get_movies():
    movies = mongo.db.movies.find()
    response = json_util.dumps(movies)
    return Response(response, mimetype="application/json")

# MOSTRAR  {ID} movies  "GET"  ################################

@app.route('/movies/<id>', methods=['GET'])
def get_movie(id):
    print(id)
    movies = mongo.db.movies.find_one({'_id': ObjectId(id), })
    response = json_util.dumps(movies)
    return Response(response, mimetype="application/json")

# ELIMINAR  {ID} movies  "GET"  ################################

@app.route('/movies/<id>', methods=['DELETE'])
def delete_movies(id):
    mongo.db.movies.delete_one({'_id': ObjectId(id)})
    response = jsonify({'message': 'Pelicula ' + id + ' eliminada exitosamente'})
    response.status_code = 200
    return response

# UPDATE  {ID} movies  "GET"  ################################

@app.route('/movies/<_id>', methods=['PUT'])
def update_movies(_id):
    
    title = request.json['title']
    valoracion = request.json['valoracion']
    descripcion = request.json['descripcion']
    creation =  request.json['creation']

    if title and valoracion and descripcion and creation and _id:
        mongo.db.movies.update_one(
            {'_id': ObjectId(_id['$oid']) if '$oid' in _id else ObjectId(_id)}, {'$set': {'title': title,'valoracion':valoracion, 'descripcion': descripcion, 'creation': creation}})
        response = jsonify({'message': 'Pelicula ' + _id + ' actualizada exitosamente'})
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