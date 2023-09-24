from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from sqlalchemy_serializer import SerializerMixin

db = SQLAlchemy()

class Pizza(db.Model, SerializerMixin):
    __tablename__ = 'pizzas'
    
    serialize_rules = ('-restaurants.pizza',)
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable = False, unique = True)
    ingridients = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    
    
    restaurants = db.relationship(
        "Restaurant", secondary = "restaurant_pizzas" , back_populates="pizzas"
    ) 
    def __repr__(self):
        return f'<Pizza {self.name} >'



class Restaurant(db.Model, SerializerMixin):
    __tablename__ = 'restaurants'
    
    serialize_rules = ('-pizzas.restaurant',)
    
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable = False, unique = True)
    address = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    
    pizzas = db.relationship(
        "Pizza", secondary = "restaurant_pizzas" , back_populates = "restaurants"    
    )
    
    @validates('name')
    def validate_name(self, key, name):
        if len(name) > 50:
            raise ValueError("Name is too long")
        
        
    def __repr__(self):
        return f'<Pizza {self.name} >'
    
    
class RestaurantPizza(db.Model, SerializerMixin):
    __tablename__ = 'restaurant_pizzas'
    
    serialize_rules = ('-pizza.restaurants', 'restaurant.pizzas',)
    
    id = db.Column(db.Integer, primary_key=True)
    pizza_id = db.Column(db.Integer, db.ForeignKey("pizzas.id"))
    restaurant_id = db.Column(db.Integer , db.ForeignKey("restaurants.id"))
    price = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    
    @validates("price")
    def validate_price(self, key, price):
        if not(price >= 1 and price <=30):
            raise ValueError("The price is not in the acceptable range!")
        return price

