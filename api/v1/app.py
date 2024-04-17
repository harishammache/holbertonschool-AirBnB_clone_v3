#!/usr/bin/python3
"""
    create and envirnment variable and a variable app instance of flask
"""


from flask import Flask, jsonify
from models import storage
from flask_cors import CORS
from api.v1.views import app_views
from os import getenv

# create a flask application instance
app = Flask(__name__)

# Enable Cross-Origin Resource Sharing (CORS) for the Flask application.
CORS(app, resources={r"/api/*": {"origins": "0.0.0.0"}})

# register the blueprint
app.register_blueprint(app_views)


# appelle la fonction page_not_found quand flask rencontre une erreur 404
@app.errorhandler(404)
def page_not_found(error):
    """ Error handler for 404 (Not Found) errors"""
    # creer une réponse json pour l'erreur 404
    response = jsonify({"error": "Not found"})
    # definis le code d'état http sur 404
    response.status_code = 404
    return response


@app.teardown_appcontext
def close_storage(exception=None):
    """call the storage"""
    storage.close()


if __name__ == "__main__":
    # retrieve host and port environment variable
    host = getenv('HBNB_API_HOST', '0.0.0.0')
    port = getenv('HBNB_API_PORT', '5000')
    # run the flask application with threading enabled
    app.run(host=host, port=port, threaded=True)
