from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager
from marshmallow import ValidationError

from ma import ma
from db import db
from blocklist import BLOCKLIST
from resources.user import (
    UserRegister, 
    UserLogin, 
    User, 
    TokenRefresh, 
    UserLogout, 
    UserConfirm)
from resources.item import Item, ItemList
from resources.store import Store, StoreList

#def create_app(db_url=None):
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["PROPAGATE_EXCEPTIONS"] = True
app.secret_key = "jose"  # could do app.config['JWT_SECRET_KEY'] if we prefer
api = Api(app)


#@app.before_first_request
# create_tables function 
db.init_app(app)
with app.app_context():
    db.create_all()

@app.errorhandler(ValidationError)
def handle_marshmallow_validation(err): # except ValidationError as err
    return jsonify(err.messages), 400

ma.init_app(app)

jwt = JWTManager(app)

# This method will check if a token is blocklisted, and will be called automatically when blocklist is enabled
@jwt.token_in_blocklist_loader
def check_if_token_in_blocklist(jwt_header, jwt_payload):
    return jwt_payload["jti"] in BLOCKLIST

api.add_resource(Store, "/store/<string:name>")
api.add_resource(StoreList, "/stores")
api.add_resource(Item, "/item/<string:name>")
api.add_resource(ItemList, "/items")
api.add_resource(UserRegister, "/register")
api.add_resource(User, "/user/<int:user_id>")
api.add_resource(UserLogin, "/login")
api.add_resource(TokenRefresh, "/refresh")
api.add_resource(UserLogout, "/logout")
api.add_resource(UserConfirm, "/user_confirm/<int:user_id>")

if __name__ == "__main__":
    app.run(port=5000, debug=True)
