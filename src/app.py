# imports
from email import message
from flask import Flask, jsonify, request, Response
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash
from bson import ObjectId, json_util


# config
app = Flask(__name__)
app.config['MONGO_URI']='mongodb://localhost/APIPython'
mongo = PyMongo(app)


# helpers
@app.errorhandler(404)
def not_found(error=None):
    response = jsonify({
        'message': 'Resource not found: ' + request.url,
        'status': 404
    })
    response.status_code = 404
    return response 




# routes
@app.route('/users', methods=['POST'])
def create_user():

    # receiving data
    username = request.json['username']
    password = request.json['password']
    email = request.json['email']

    # verificando si existe
    user = mongo.db.users.find_one({"email":request.json['email']})
    if user:
        return {'message': 'Registered user'}
    else:
        # guardamos el usuario que recibimos, no tenemos validacion de si existe el usuario al momento. 
        if username and email and password:
            # antes de guardar el password lo volvemos hash
            hashed_password = generate_password_hash(password)
            id = mongo.db.users.insert_one(
                {'username':username, 'password': hashed_password, 'email': email }
            ).inserted_id                       # el .insert_id hace que podamos devolver con la response el id. 
            response = {
                'id': str(id),                  # str(id) pasa a String el ObjectId que viene con la respuesta de la base de datos
                'username': username,
                'password': password,
                'email': email,
            } 
            print(response)
            return response
        else:
            return not_found() # utilizamos la funcion que creamos para manejar el err / Si los recursos no llegan o falto algo manejamos asi el err
        
    return {'message': 'Data user received'}
        
        
    
@app.route('/users', methods=['GET'])
def get_users():
    users = mongo.db.users.find() # querie de mongo para obtener los datos de esa coleccion, devuelve en formato bson
    # devolvemos la lista en formato json con la libreria selecionado
    response = json_util.dumps(users) # utilizamos el metodo dump que convierte en json y lo almacenamos en una variable llamada response
    # utilizamos Response de flask para advertir al cliente el tipo de dato que recibe, devolvemos una respose mas elaborada
    return Response(response, mimetype='application/json')



@app.route('/users/<id>', methods=['GET'])
def get_user(id):
    user = mongo.db.users.find_one({
        '_id': ObjectId(id) # convertimos en ObjectId el id que nos estan pasando, dado que recibimos un string
    })
    if user: 
        response = json_util.dumps(user)
        return Response(response, mimetype='application/json')
    else:
        return {'message': 'User id: ' + id + ' Not Found'} # como la response de users, la volvemos mas elaborada la response
    
    
    
@app.route('/users/<id>', methods=['DELETE'])
def delete_user(id):
    user = mongo.db.users.find_one_and_delete({
        '_id': ObjectId(id) # convertimos en ObjectId el id que nos estan pasando, dado que recibimos un string
    })
    print(user)
    print(id)
    
    if user:
        return {'message': 'User id: ' + id + ' was deleted'} # response de borrado de user
    else:
        return not_found()


@app.route('/users/<id>', methods=['PUT'])
def update_user(id):
    # receiving data
    username = request.json['username']
    password = request.json['password']
    email = request.json['email']

    if username and email and password:
        hashed_password = generate_password_hash(password)
        mongo.db.users.update_one({'_id': ObjectId(id)}, {'$set': {
            'username': username,
            'password': hashed_password,
            'email': email
        }})
        response = jsonify({'message': 'User' + id + ' was updated successfully'})
        return response



# server
if __name__ == "__main__":
    app.run(debug=True)
