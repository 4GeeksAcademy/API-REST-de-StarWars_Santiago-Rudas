import os
from flask import Flask, request, jsonify
from flask_migrate import Migrate
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Character, Planet, FavoritePlanet, FavoriteCharacter
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.url_map.strict_slashes = False

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Configuración de base de datos
db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicialización
db.init_app(app)
migrate = Migrate(app, db)   # primero db.init_app, luego migrate
CORS(app)
setup_admin(app)

# Manejo de errores
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# Sitemap
@app.route('/')
def sitemap():
    return generate_sitemap(app)

# ---------------- USERS ---------------- #
@app.route('/user', methods=['GET'])
def get_all_users():
    users = User.query.all()
    users_serialized = [user.serialize() for user in users]
    return jsonify({'msg': 'OK', 'user': users_serialized}), 200

@app.route('/user/<int:id>', methods=['GET'])
def get_single_user(id):
    user = User.query.get(id)
    if user is None:
        return jsonify({'msg': f'El usuario con id {id} no existe'}), 404
    return jsonify({'msg': 'ok', 'user': user.serialize()}), 200

@app.route('/user', methods=['POST'])
def create_user():
    body = request.get_json(silent=True)
    if body is None:
        return jsonify({'msg': ' Debes enviar info en el body'}), 400
    
    required_fields = ['name', 'last_name', 'password', 'email']
    for field in required_fields:
        if field not in body:
            return jsonify({'msg': f'el campo {field.upper()} es obligatorio'}), 400
    
    new_user = User(
        name=body['name'],
        last_name=body['last_name'],
        password=body['password'],
        email=body['email'],
        is_active=True
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'msg': 'OK', 'user': new_user.serialize()}), 201

# ---------------- CHARACTERS ---------------- #
@app.route('/characters', methods=['GET'])
def get_all_characters():
    characters = Character.query.all()
    return jsonify({'msg': 'OK', 'character': [c.serialize() for c in characters]})

@app.route('/characters/<int:id>', methods=['GET'])
def get_single_character(id):
    character = Character.query.get(id)
    if character is None:
        return jsonify({'msg': 'No existe un personaje para ese ID'}), 404
    return jsonify({'msg': 'OK', 'character': character.serialize()})

# ---------------- PLANETS ---------------- #
@app.route('/planets', methods=['GET'])
def get_all_planets():
    planets = Planet.query.all()
    return jsonify({'msg': 'OK', 'planet': [p.serialize() for p in planets]})

@app.route('/planets/<int:id>', methods=['GET'])
def get_single_planet(id):
    planet = Planet.query.get(id)
    if planet is None:
        return jsonify({'msg':'No existe un planeta con el Id indicado'}), 404
    return jsonify({'msg':'OK', 'planet': planet.serialize()})

# ---------------- FAVORITES ---------------- #
@app.route('/users/<int:id_user>/favorites', methods=['GET'])
def get_user_favorites(id_user):
    user = User.query.get(id_user)
    if user is None:
        return jsonify({'msg': 'El ID proporcionado no esta asociado a ningun usuario'}), 404

    characters_favorites_serialized = [fav.character.serialize() for fav in user.favorites_characters]
    planets_favorites_serialized = [fav.planet.serialize() for fav in user.favorites_planets]

    return jsonify({'msg': 'OK', 'favorite_characters': characters_favorites_serialized, 'favorite_planets': planets_favorites_serialized})

@app.route('/favorite/<int:id_user>/planet/<int:id_planet>', methods=['POST'])
def create_favorite_planet(id_user, id_planet):
    new_favorite_planet = FavoritePlanet(user_id=id_user, planet_id=id_planet)
    db.session.add(new_favorite_planet)
    db.session.commit()
    return jsonify({'msg': 'ok', 'favorite': new_favorite_planet.serialize()})

@app.route('/favorite/<int:id_user>/character/<int:id_character>', methods=['POST'])
def create_favorite_character(id_user, id_character):
    new_favorite_character = FavoriteCharacter(user_id=id_user, character_id=id_character)
    db.session.add(new_favorite_character)
    db.session.commit()
    return jsonify({'msg': 'OK', 'Character': new_favorite_character.serialize()})

# ---------------- CREATE ---------------- #
@app.route('/planet', methods=['POST'])
def create_planet():
    body = request.get_json(silent=True)
    if body is None or 'name' not in body:
        return jsonify({'msg': 'debes enviar un NAME para el planeta'}), 400
    
    new_planet = Planet(name=body['name'])
    db.session.add(new_planet)
    db.session.commit()
    return jsonify({'msg': 'OK', 'planet': new_planet.serialize()}), 201

@app.route('/character', methods=['POST'])
def create_character():
    body = request.get_json(silent=True)
    required_fields = ['name', 'height', 'weight']
    for field in required_fields:
        if field not in body:
            return jsonify({'msg': f'debes enviar {field.upper()} para el personaje'}), 400
    
    new_character = Character(name=body['name'], height=body['height'], weight=body['weight'])
    db.session.add(new_character)
    db.session.commit()
    return jsonify({'msg': 'OK', 'character': new_character.serialize()}), 201

# ---------------- UPDATE ---------------- #
@app.route('/planet/<int:id_planet>', methods=['PUT'])
def update_planet(id_planet):
    planet_to_update = Planet.query.get(id_planet)
    if planet_to_update is None:
        return jsonify({'msg': 'El id del planeta no fue encontrado'}), 404
    
    body = request.get_json()
    if 'name' in body:
        planet_to_update.name = body['name']
    db.session.commit()

    return jsonify({'msg': 'ok', 'planet': planet_to_update.serialize()})

# ---------------- RUN ---------------- #
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
