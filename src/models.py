from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, Integer, ForeignKey, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()

# ---------------------------
# TABLAS DE ASOCIACIÓN
# ---------------------------

character_film = Table(
    "character_film",
    db.Model.metadata,
    db.Column("character_id", ForeignKey("character.id"), primary_key=True),
    db.Column("film_id", ForeignKey("film.id"), primary_key=True),
)

planet_film = Table(
    "planet_film",
    db.Model.metadata,
    db.Column("planet_id", ForeignKey("planet.id"), primary_key=True),
    db.Column("film_id", ForeignKey("film.id"), primary_key=True),
)

starship_film = Table(
    "starship_film",
    db.Model.metadata,
    db.Column("starship_id", ForeignKey("starship.id"), primary_key=True),
    db.Column("film_id", ForeignKey("film.id"), primary_key=True),
)

character_starship = Table(
    "character_starship",
    db.Model.metadata,
    db.Column("character_id", ForeignKey("character.id"), primary_key=True),
    db.Column("starship_id", ForeignKey("starship.id"), primary_key=True),
)

# ---------------------------
# MODELOS PRINCIPALES
# ---------------------------

class User(db.Model):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(80), nullable=False)
    last_name: Mapped[str] = mapped_column(String(80), nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), default=True, nullable=False)

    favorites_characters: Mapped[list["FavoriteCharacter"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )
    favorites_planets: Mapped[list["FavoritePlanet"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )
    favorites_starships: Mapped[list["FavoriteStarship"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "last_name": self.last_name,
            "email": self.email,
            "is_active": self.is_active,
        }


class Character(db.Model):
    __tablename__ = "character"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    height: Mapped[str] = mapped_column(String(10))
    mass: Mapped[str] = mapped_column(String(10))
    hair_color: Mapped[str] = mapped_column(String(50))
    skin_color: Mapped[str] = mapped_column(String(50))
    eye_color: Mapped[str] = mapped_column(String(50))
    birth_year: Mapped[str] = mapped_column(String(20))
    gender: Mapped[str] = mapped_column(String(20))

    homeworld_id: Mapped[int] = mapped_column(ForeignKey("planet.id"))
    homeworld: Mapped["Planet"] = relationship(back_populates="residents")

    films: Mapped[list["Film"]] = relationship(
        secondary=character_film, back_populates="characters"
    )
    starships: Mapped[list["Starship"]] = relationship(
        secondary=character_starship, back_populates="pilots"
    )

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "height": self.height,
            "mass": self.mass,
            "hair_color": self.hair_color,
            "skin_color": self.skin_color,
            "eye_color": self.eye_color,
            "birth_year": self.birth_year,
            "gender": self.gender,
            "homeworld": self.homeworld.name if self.homeworld else None,
        }


class Planet(db.Model):
    __tablename__ = "planet"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    rotation_period: Mapped[str] = mapped_column(String(20))
    orbital_period: Mapped[str] = mapped_column(String(20))
    diameter: Mapped[str] = mapped_column(String(20))
    climate: Mapped[str] = mapped_column(String(50))
    gravity: Mapped[str] = mapped_column(String(50))
    terrain: Mapped[str] = mapped_column(String(50))
    surface_water: Mapped[str] = mapped_column(String(20))
    population: Mapped[str] = mapped_column(String(50))

    residents: Mapped[list["Character"]] = relationship(back_populates="homeworld")
    films: Mapped[list["Film"]] = relationship(
        secondary=planet_film, back_populates="planets"
    )

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "rotation_period": self.rotation_period,
            "orbital_period": self.orbital_period,
            "diameter": self.diameter,
            "climate": self.climate,
            "gravity": self.gravity,
            "terrain": self.terrain,
            "surface_water": self.surface_water,
            "population": self.population,
        }


class Starship(db.Model):
    __tablename__ = "starship"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    model: Mapped[str] = mapped_column(String(100))
    manufacturer: Mapped[str] = mapped_column(String(200))
    cost_in_credits: Mapped[str] = mapped_column(String(50))
    length: Mapped[str] = mapped_column(String(50))
    max_atmosphering_speed: Mapped[str] = mapped_column(String(50))
    crew: Mapped[str] = mapped_column(String(50))
    passengers: Mapped[str] = mapped_column(String(50))
    cargo_capacity: Mapped[str] = mapped_column(String(50))
    consumables: Mapped[str] = mapped_column(String(50))
    hyperdrive_rating: Mapped[str] = mapped_column(String(20))
    MGLT: Mapped[str] = mapped_column(String(20))
    starship_class: Mapped[str] = mapped_column(String(50))

    pilots: Mapped[list["Character"]] = relationship(
        secondary=character_starship, back_populates="starships"
    )
    films: Mapped[list["Film"]] = relationship(
        secondary=starship_film, back_populates="starships"
    )

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "model": self.model,
            "manufacturer": self.manufacturer,
            "cost_in_credits": self.cost_in_credits,
            "length": self.length,
            "max_atmosphering_speed": self.max_atmosphering_speed,
            "crew": self.crew,
            "passengers": self.passengers,
            "cargo_capacity": self.cargo_capacity,
            "consumables": self.consumables,
            "hyperdrive_rating": self.hyperdrive_rating,
            "MGLT": self.MGLT,
            "starship_class": self.starship_class,
        }


class Film(db.Model):
    __tablename__ = "film"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)

    characters: Mapped[list["Character"]] = relationship(
        secondary=character_film, back_populates="films"
    )
    planets: Mapped[list["Planet"]] = relationship(
        secondary=planet_film, back_populates="films"
    )
    starships: Mapped[list["Starship"]] = relationship(
        secondary=starship_film, back_populates="films"
    )

    def serialize(self):
        return {"id": self.id, "title": self.title}


# ---------------------------
# FAVORITOS (Usuarios)
# ---------------------------

class FavoriteCharacter(db.Model):
    __tablename__ = "favorite_character"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    character_id: Mapped[int] = mapped_column(ForeignKey("character.id"))

    user: Mapped["User"] = relationship(back_populates="favorites_characters")
    character: Mapped["Character"] = relationship()

    def serialize(self):
        return {
            "id": self.id,
            "character": self.character.serialize() if self.character else None,
        }


class FavoritePlanet(db.Model):
    __tablename__ = "favorite_planet"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    planet_id: Mapped[int] = mapped_column(ForeignKey("planet.id"))

    user: Mapped["User"] = relationship(back_populates="favorites_planets")
    planet: Mapped["Planet"] = relationship()

    def serialize(self):
        return {
            "id": self.id,
            "planet": self.planet.serialize() if self.planet else None,
        }


class FavoriteStarship(db.Model):
    __tablename__ = "favorite_starship"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    starship_id: Mapped[int] = mapped_column(ForeignKey("starship.id"))

    user: Mapped["User"] = relationship(back_populates="favorites_starships")
    starship: Mapped["Starship"] = relationship()

    def serialize(self):
        return {
            "id": self.id,
            "starship": self.starship.serialize() if self.starship else None,
        }
