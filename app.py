from flask import Flask, request, abort
from flask_restful import Api, Resource, reqparse
from views import views

app = Flask(__name__)

# Initalizes REST API
api = Api(app)

# Validates user input to ensure correct arguments were given
address_get_args = reqparse.RequestParser()
address_get_args.add_argument("street", type=str, help="You did not provide a street address", required=True)
address_get_args.add_argument("city", type=str, help="You did not provide a city", required=True)
address_get_args.add_argument("state", type=str, help="You did not provide a state", required=True)

address = {"street": "street", "city": "city", "state": "state"}

electeds = {}

response = request.get('https://www.usa.gov/elected-officials')


# Checks to see if address is in database.
# NEEDS TO GO IN GET OR PUT METHODS BELOW IDK WHICH
def abort_if_no_address_hits(address):
    if address not in address:
        abort(404, message="Address provided is not valid")


# Creating a resource class to handle GET/PUT/DELETE Requests
class Address(Resource):
    def get(self, address):
        # args = address_get_args.parse_args()
        return address

    def put(self, address):
        args = address_get_args.parse_args()
        print(args)
        return address


class Elected(Resource):
    def get(self, elected_id):
        # print(request.form)
        return electeds[elected_id]


# Adds classes to the API
# When sending a get request to "/electeds, we reiceved back "[address]" information
api.add_resource(Address, "/results/<string:address>")

api.add_resource(Elected, "/congress/<int:elected_id>")

# Pulls webpages from views.py file
app.register_blueprint(views, url_prefix="/")

if __name__ == '__main__':
    app.run(debug=True, port=8000)
