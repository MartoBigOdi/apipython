# imports
from flask import Flask, request
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash


# config
app = Flask(__name__)
app.config['MONGO_URI']='mongodb://localhost/APIPython'
mongo = PyMongo(app)


# routes
@app.route('/users', methods=['POST'])
def create_user():
    # receiving data
    username = request.json['username']
    password = request.json['password']
    email = request.json['email']

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
         {'message': 'Data user not received'}
    return {'message': 'Data user received'}
    
    
# server
if __name__ == "__main__":
    app.run(debug=True)
