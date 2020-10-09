from flask import Flask, jsonify, request, Response
from flask_pymongo import PyMongo
from bson import json_util
from bson.objectid import ObjectId
import json


app = Flask(__name__)

app.secret_key = 'masterkey'

app.config['MONGO_URI'] = 'mongodb://192.168.99.100:27017/showtimes'


mongo = PyMongo(app)

## CREATE  showtimes  "POST" #############################

@app.route('/showtimes', methods=['POST'])
def create_showtimes():
    # Receiving Data
    fecha = request.json['fecha']
    movies = request.json['movies']
    
    if fecha and movies :
        
        id = mongo.db.showtimes.insert(
            {'fecha': fecha,'movies':movies})
        response = jsonify({
            '_id': str(id),
            'fecha': fecha,
            'movies':movies
        })
        response.status_code = 201
        return response
    else:
        return not_found()

# MOSTRAR showtimes  "GET"  ################################

@app.route('/showtimes', methods=['GET'])
def get_showtimes():
    showtimes = mongo.db.showtimes.find()
    response = json_util.dumps(showtimes)
    return Response(response, mimetype="application/json")

# MOSTRAR  {ID} showtimes  "GET"  ################################

@app.route('/showtimes/<id>', methods=['GET'])
def get_showtime(id):
    print(id)
    showtimes = mongo.db.showtimes.find_one({'_id': ObjectId(id), })
    response = json_util.dumps(showtimes)
    return Response(response, mimetype="application/json")

# ELIMINAR  {ID} showtimes  "GET"  ################################

@app.route('/showtimes/<id>', methods=['DELETE'])
def delete_showtimes(id):
    mongo.db.showtimes.delete_one({'_id': ObjectId(id)})
    response = jsonify({'message': 'Horario ' + id + ' eliminado exitosamente'})
    response.status_code = 200
    return response

# UPDATE  {ID} showtimes  "PUT"  ################################

@app.route('/showtimes/<_id>', methods=['PUT'])
def update_showtimes(_id):
    fecha = request.json['fecha']
    movies = request.json['movies']
 
    if fecha and movies:
        
        mongo.db.showtimes.update_one(
            {'_id': ObjectId(_id['$oid']) if '$oid' in _id else ObjectId(_id)}, {'$set': {'fecha': fecha,'movies':movies}})
        response = jsonify({'message': 'Horario ' + _id + ' actualizado exitosamente'})
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