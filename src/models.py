from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


# Tabla intermedia para User y FavoritePeople 
favorite_people_table = db.Table(
    'favorite_people_table',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('people_id', db.Integer, db.ForeignKey('people.uid'), primary_key=True)
)

# Tabla intermedia para User y FavoritePlanets
favorite_planets_table = db.Table(
    'favorite_planets_table',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('planet_id', db.Integer, db.ForeignKey('planets.uid'), primary_key=True)
)





class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    favorite_people = db.relationship('People', secondary=favorite_people_table, backref='users_favorite')
    favorite_planets = db.relationship('Planets', secondary=favorite_planets_table, backref='users_favorite')
    
    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }
    

class People(db.Model):
    __tablename__ = "people"
    uid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    description = db.Column(db.String(), unique=False, nullable=False)
    eyes_color = db.Column(db.String(80), unique=False, nullable=False)
   


    def __repr__(self):
        return '<People %r>' % self.name
    def serialize(self):
        return {
            "id": self.uid,
            "name": self.name,
            "description": self.description,
            "eyes_color": self.eyes_color,
        }
    


class Planets(db.Model):
    __tablename__ = "planets"
    uid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    description = db.Column(db.String(), unique=False, nullable=False)
    population = db.Column(db.String(80), unique=False, nullable=False)
    

    def __repr__(self):
        return '<Planets %r>' % self.name

    def serialize(self):
        return {
            "id": self.uid,
            "name": self.name,
            "description": self.description,
            "population": self.population,
            
            
        }



# class FavoritePeople(db.Model): 
#       __tablename__ = "favoritepeople"
#       id = db.Column(db.Integer, primary_key=True)
#       user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
#       people_id = db.Column(db.Integer, db.ForeignKey("people.uid"))
      
      

#       def __repr__(self):
#           return '<Favorite_People %r>' % self.id
      
#       def serialize(self):
#           return {
#               "id": self.id,
#               "user_id": self.user_id,
#               "people_id": self.people_id
#           }        
    
# class FavoritePlanets(db.Model): 
#       __tablename__ = "favoriteplanets"
#       id = db.Column(db.Integer, primary_key=True)
#       user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
#       planet_id = db.Column(db.Integer, db.ForeignKey("planets.uid"))

#       def __repr__(self):
#           return '<Favorite_Planets %r>' % self.id
      
#       def serialize(self):
#           return {
#               "id": self.id,
#               "user_id": self.user_id,
#               "planet_id": self.planet_id
#           }
      


