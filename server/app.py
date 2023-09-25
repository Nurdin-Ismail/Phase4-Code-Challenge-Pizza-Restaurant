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

class Restaurants(Resource):
    
    def get(self):
        restaurants_dict = [n.to_dict() for n in Restaurant.query.all()]
        return make_response(jsonify(restaurants_dict), 200)

api.add_resource(Restaurants, '/restaurants')

class RestaurantbyID(Resource):
    
    def get(self, id):
        restaurant = Restaurant.query.filter_by(id=id).first()
        
        restaurant_dict =restaurant.to_dict()
        
        
        return make_response(jsonify(restaurant_dict), 200)
    
    def delete(self,id):
        
        restaurant = Restaurant.query.filter_by(id=id).first()
        if restaurant:
            db.session.delete(restaurant)
            db.session.commit()

            response = {
                "delete-successful":True,
                "message": "restaurant deleted"
            }
            return make_response(jsonify(response),204)
        
        else:
            response = { "error": "restaurant you are trying to delete DOES NOT EXIST" }
            return make_response(response,404)


api.add_resource(RestaurantbyID, '/restaurants/<int:id>')

class Pizzas(Resource):
    
    def get(self):
        pizzas_dict = [n.to_dict() for n in Pizza.query.all()]
        return make_response(jsonify(pizzas_dict), 200)
    
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


        rp_dict = restaurant_pizza.to_dict()
        if rp_dict:
            return make_response(rp_dict,201)
        else:
            response ={"errors": ["validation errors"] }
            return make_response(restaurant_pizza, 404)
    
api.add_resource(RestaurantPizzas, '/restaurant_pizzas')
    



if __name__ == '__main__':
    app.run(port=5555, debug=True)