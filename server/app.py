#!/usr/bin/env python3


from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pizza_restaurant.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

@app.route('/')
def home ():
    response = {
        "Message":"Pizza Restaurant API.",
        "Pizza_Endpoint": '/pizzas',
        "Restaurants_Endpoint": '/restaurants',
        }
    return make_response(response, 200)

class Restaurants(Resource):
    # Queries for all records for restaurants
    def get(self):
        restaurants = []
        for restaurant in Restaurant.query.all():
            restaurant_dict = {
                'id' : restaurant.id,
                'name' : restaurant.name,
                'address' : restaurant.address
            }
            
            restaurants.append(restaurant_dict)
        return make_response(jsonify(restaurants), 200)

api.add_resource(Restaurants, '/restaurants')

class RestaurantbyID(Resource):
    # Queries for specific restaurant and either gets them or deletes them based o the HTTP verb
    def get(self, id):
        restaurant = Restaurant.query.filter_by(id=id).first()
        if restaurant:
             restaurant_dict =restaurant.to_dict()
             return make_response(jsonify(restaurant_dict), 200)
        else:
            response = { "error": "restaurant you are trying to get DOES NOT EXIST" }
            return make_response(response,404)
        
        
    
    def delete(self,id):
        # Queries for specified restaurant
        restaurant = Restaurant.query.filter_by(id=id).first()
        # Queries for all records with specified restaurant id
        restaurant_pizzas = RestaurantPizza.query.filter_by(restaurant_id = restaurant.id).all()
        if restaurant_pizzas:
            
            # Deletes all records containing the restaurant's id
            for n in restaurant_pizzas:
                
                db.session.delete(n)
                db.session.commit()
        
        # Checks if restaurant is real and if it is, then it 
        # Deletes the restaurant and returns successful response
        if restaurant:
            db.session.delete(restaurant)
            db.session.commit()
            restaurant = Restaurant.query.filter_by(id=id).first()
            
            if not restaurant:
                responso = {
                "delete-successful":True,
                "message": "restaurant deleted"
            }
                return make_response(jsonify(responso))

            
        
        else:
            response = { "error": "restaurant you are trying to delete DOES NOT EXIST" }
            return make_response(response,404)


api.add_resource(RestaurantbyID, '/restaurants/<int:id>')

class Pizzas(Resource):
    # Queries for all pizza records and returns them as a response
    def get(self):
        pizzas = []
        for pizza in Pizza.query.all():
            pizza_dict = {
                'id' : pizza.id,
                'name' : pizza.name,
                'ingridients' : pizza.ingridients
            }
            
            pizzas.append(pizza_dict)
        return make_response(jsonify(pizzas), 200)
    
api.add_resource(Pizzas, '/pizzas')

class RestaurantPizzas(Resource):
    
    def post(self):
        restaurant_pizza = RestaurantPizza(
            
            pizza_id= request.form.get('pizza_id'),
            restaurant_id=request.form.get('restaurant_id'),
            price =int(request.form.get('price')),
        
        )
        
        
        db.session.add(restaurant_pizza)
        db.session.commit()

        # Turns record data into a dictionary
        rp_dict = restaurant_pizza.to_dict()
        if rp_dict:
            # send back a response with the data related to the Pizza
            return make_response(rp_dict['pizza'],201)
        else:
            response ={"errors": ["validation errors"] }
            return make_response(restaurant_pizza, 404)
    
api.add_resource(RestaurantPizzas, '/restaurant_pizzas')
    



if __name__ == '__main__':
    app.run(port=5555, debug=True)