from flask import Flask, request        # need requests for when Postman gets requests and does something with POST METHOD IT
from flask_restful import Resource, Api, reqparse # don't need jsonify for flask_restful because it's reads in JSON IT
from flask_jwt import JWT, jwt_required  ## something with authentication IT. Did this with authentication part of video

from security import authenticate, identity  ## did this when in the make authentication login part of video

app = Flask(__name__)
app.secret_key = "Jose"  # pip install Flask-JWT.  "Jose" will be the secret key for authentification.
api = Api(app)

jwt = JWT(app, authenticate, identity)   ## JWT created new endpoint /auth  ## creates an object for authentication IT. ## authencification part of video

items = []

class Item(Resource):  # the class should be capital IT
    parser = reqparse.RequestParser()  #### Optimizing code: the parser now belongs to the class itself and not one specific item resource.
    parser.add_argument("price",  ### we are parsing the price in this case
                        type=float,
                        required=True,  ### no request can come through with no price
                        help="This Field cannot be left blank!"
                        )

    @jwt_required()     ## forces client to authenticate before method gets called. You can put in front of any METHOD.
    def get(self, name):
        # looks like x would be items and lamda loops through them IT. Filter function has 2 arguments.
        # filter return filter object that methods can be called upon.
        # So, you can do list(filter(lambda x: x["name"] == name, items)) if you wanted to return a list.
        # since you only want 1 item for this exercise you can do next which will pull up first item.
        # you can call next again by calling over and over and over if you want.
        # it can also raise and error if there are no more items left. So, you need to break it with None:  code: next(xxxx,None)
        item = next(filter(lambda x: x["name"] == name, items), None)
        return {"item": item}, 200 if item else 404  # STATUS CODE: if item exists and 404 if it's not found

    def post(self, name):
        data = Item.parser.parse_args()  # to call and use the parser you add Item capitalized
        if next(filter(lambda x: x["name"] == name, items), None):  # finds if an item matches the name; already exists.
            return {"message": "An item with name '{}' already exists.".format(name)}, 400  # STATUS CODE: 400 bad request, request for name already in server. Clients fault.


        data = request.get_json()  # request will have a JSON body attached to it. Request must have JSON body
                                   # or header conten type must be json
        # If your not sure it your clients are going to give you JSON or not you can prevent from giving an error
        # data = request.get_json(force=True)  # will not look at header which maybe isn't good
        # data = request.get_json(silent=True) # won't return an error but just returns none
        item = {"name": name, "price": data["price"]}
        items.append(item)
        return item, 201 # STATUS CODE: for when an object is created and added to the database

    def delete(self, name):
        global items    ## it will solve the code line below. It means to use the outside variable of the whole code block (line 13)
        items = list(filter(lambda x: x["name"] != name, items))  # this won't work because python gets confused from renaming items object. need to add global above

    def put(self, name):
        data = Item.parser.parse_args()
        # data = request.get_json()   ### was replaced with above line because we then added ResquestParser which then got moved again to the top below the Item class
        item = next(filter(lambda x: x["name"] == name, items), None)
        if item is None:
            item = {"name": name, "price": data["price"]}
            items.append(item)
        else:
            item.update(data)   # dictionaries have an update method. data variable is a dictionary.
        return item

class ItemList(Resource):    # the class should be capital IT
    def get(self):
        return {"items": items}

api.add_resource(Item, "/item/<string:name>") # ADDS THE RESOURCE http://127.0.0.1:5000/student/Rolf
api.add_resource(ItemList, "/items")             # ADDS THE RESOURCE http://127.0.0.1:5000/items

# default port is 5000
# you can also write app.run(port=5000) if you want
app.run(port=5000, debug=True) # puts a good error page on html page saying what's wrong