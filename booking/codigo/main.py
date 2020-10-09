from flask import Flask, jsonify, request, Response
from flask_pymongo import PyMongo
from bson import json_util
from bson.objectid import ObjectId
import json



app = Flask(__name__)

app.secret_key = 'masterkey'

app.config['MONGO_URI'] = 'mongodb://192.168.99.100:27017/booking'


mongo = PyMongo(app)

## CREATE  booking  "POST" #############################

@app.route('/booking', methods=['POST'])
def create_booking():
    # Receiving Data
    userID = request.json['userID']
    showtimesID = request.json['showtimesID']
    movies = request.json['movies']
    

    if userID and showtimesID and movies:
        id = mongo.db.booking.insert(
            {'userID': userID,'showtimesID':showtimesID, 'movies':movies})
        response = jsonify({
            '_id': str(id),
            'userID': userID,
            'showtimesID':showtimesID,
            'movies': movies          
        })
        response.status_code = 201
        return response
    else:
        return not_found()

# MOSTRAR booking  "GET"  ################################

@app.route('/booking', methods=['GET'])
def get_bookings():
    booking = mongo.db.booking.find()
    response = json_util.dumps(booking)
    return Response(response, mimetype="application/json")

# MOSTRAR  {ID} booking  "GET"  ################################

@app.route('/booking/<id>', methods=['GET'])
def get_booking(id):
    print(id)
    booking = mongo.db.booking.find_one({'_id': ObjectId(id), })
    response = json_util.dumps(booking)
    return Response(response, mimetype="application/json")

# ELIMINAR  {ID} booking  "GET"  ################################

@app.route('/booking/<id>', methods=['DELETE'])
def delete_booking(id):
    mongo.db.booking.delete_one({'_id': ObjectId(id)})
    response = jsonify({'message': 'Reserva ' + id + ' eliminada exitosamente'})
    response.status_code = 200
    return response


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