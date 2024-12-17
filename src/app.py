"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User,People,Planets
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)



#USERS GET

@app.route('/user', methods=['GET'])
def get_users():

    users = User.query.all()
    users_list = [user.serialize() for user in users]

    return jsonify(users_list), 200



#USER POST

@app.route('/user', methods=['POST'])
def create_user():
    request_body = request.get_json()
    exist = User.query.filter_by(email = request_body['email']).first()
    if exist:
        return jsonify({"msg:": "Este usuario ya existe"})
    new_user = User(email= request_body ["email"], password= request_body["password"], is_active = True)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"msg": "Usuario creado con éxito"})






#PEOPLE GET

@app.route("/people", methods = ["GET"])
def get_people():
        
        people = People.query.all()
        people_list = [char.serialize() for char in people]

        return jsonify (people_list), 200
      


#PEOPLE POST

@app.route('/people/create', methods=['POST'])
def create_people():
    request_body = request.get_json()
    exist = People.query.filter_by(name = request_body['name']).first()
    if exist:
        return jsonify({"msg:": "Este personaje ya existe"})
    new_char = People (name= request_body["name"], description= request_body["description"], eyes_color= request_body["eyes_color"])
    db.session.add(new_char)
    db.session.commit()
    return jsonify({"msg": "Personaje creado con éxito"})
        

 



#CHARACTER GET

@app.route("/people/<int:people_id>", methods = ["GET"]) 
def get_character(people_id):
        
        character = People.query.get(people_id)
        if not character:
            return jsonify({"msg": "Personaje no encontrado"}), 404
        return jsonify(character.serialize()), 200


#CHARACTER ADD FAVORITE

@app.route('/user/<int:user_id>/favorite/people', methods=['POST'])
def add_favorite_people(user_id):
    request_body = request.get_json()
    people_id = request_body.get("people_id")

    user = User.query.get(user_id)
    people = People.query.get(people_id)

    if not user or not people:
        return jsonify({"msg": "Usuario o personaje no encontrado"}), 404

    user.favorite_people.append(people) 
    db.session.commit()

    return jsonify({"msg": "Personaje añadido a favoritos"}), 200



#PLANETS GET

@app.route('/planets', methods=['GET'])
def get_planets():

    planets = Planets.query.all()
    planet_list = [planet.serialize() for planet in planets]

    return jsonify(planet_list), 200


#PLANET ID GET

@app.route("/planets/<int:planet_id>", methods = ["GET"]) 
def get_planet(planet_id):
        
        planet = Planets.query.get(planet_id)
        if not planet:
            return jsonify({"msg": "Planeta no encontrado"}), 404
        return jsonify(planet.serialize()), 200


# ADD FAVORITE PLANET

@app.route('/user/<int:user_id>/favorite/planets', methods=['POST'])
def add_favorite_planet(user_id):
    request_body = request.get_json()
    planet_id = request_body.get("planet_id")

    user = User.query.get(user_id)
    planet = Planets.query.get(planet_id)

    if not user or not planet:
        return jsonify({"msg": "Usuario o planeta no encontrado"}), 404

    user.favorite_planets.append(planet)  
    db.session.commit()

    return jsonify({"msg": "Planeta añadido a favoritos"}), 200



#DELETE FAVORITE PEOPLE

@app.route('/user/<int:user_id>/favorite/people/<int:people_id>', methods=['DELETE'])
def delete_favorite_people(user_id, people_id):
    user = User.query.get(user_id)
    people = People.query.get(people_id)

    if not user or not people:
        return jsonify({"msg": "Usuario o personaje no encontrado"}), 404

    user.favorite_people.remove(people)  
    db.session.commit()

    return jsonify({"msg": "Personaje eliminado de favoritos"}), 200




#DELETE FAVORITE PLANET
@app.route('/user/<int:user_id>/favorite/planets/<int:planet_id>', methods=['DELETE'])
def delete_favorite_planet(user_id, planet_id):
    user = User.query.get(user_id)
    planet = Planets.query.get(planet_id)

    if not user or not planet:
        return jsonify({"msg": "Usuario o planeta no encontrado"}), 404

    user.favorite_planets.remove(planet)  
    db.session.commit()

    return jsonify({"msg": "Planeta eliminado de favoritos"}), 200


#USER FAVORITES GET

@app.route('/user/<int:user_id>/favorites', methods=['GET'])
def get_user_favorites(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"msg": "Usuario no encontrado"}), 404
    
    favorites = {
        "favorite_people": [people.serialize() for people in user.favorite_people],
        "favorite_planets": [planet.serialize() for planet in user.favorite_planets]
    }
    return jsonify(favorites), 200



# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)





     
