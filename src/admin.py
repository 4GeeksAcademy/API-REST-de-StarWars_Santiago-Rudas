import os
from flask_admin import Admin
from models import db, User, Character, Planet, FavoriteCharacter, FavoritePlanet
from flask_admin.contrib.sqla import ModelView

class FavoriteCharacterModelView(ModelView):
    column_auto_selected_related = True
    column_list = ['id', 'user_id', 'users', 'character_id', 'character']

class FavoritePlanetModelView(ModelView):
    column_auto_selected_related = True
    column_list = ['id', 'user_id', 'users', 'planet_id', 'planet']

class UserModelView(ModelView):
    column_auto_selected_related = True
    column_list = [
        'id', 'name', 'last_name', 'email', 'password',
        'favorites_characters', 'favorites_planets', 'is_active'
    ]

class CharacterModelView(ModelView):
    column_auto_selected_related = True
    column_list = ['id', 'name', 'height', 'weight', 'favorite_character_by']

class PlanetModelView(ModelView):
    column_auto_selected_related = True
    column_list = ['id', 'name', 'favorite_planet_by']

def setup_admin(app):
    app.secret_key = os.environ.get('FLASK_APP_KEY', 'sample key')
    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
    admin = Admin(app, name='4Geeks Admin', template_mode='bootstrap3')

    # Agregamos los modelos al panel de administración
    admin.add_view(UserModelView(User, db.session))
    admin.add_view(CharacterModelView(Character, db.session))
    admin.add_view(PlanetModelView(Planet, db.session))
    admin.add_view(FavoriteCharacterModelView(FavoriteCharacter, db.session))
    admin.add_view(FavoritePlanetModelView(FavoritePlanet, db.session))
