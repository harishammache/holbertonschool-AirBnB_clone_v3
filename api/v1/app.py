"""create and envirnment variable and a variable app instance of flask"""


from flask import Flask
from models import storage
from api.v1.views import app_views
from os import getenv

# create a flask application instance
app = Flask(__name__)

# register the blueprint
app.register_blueprint(app_views, url_prefix='/api/v1')


@app.teardown_appcontext
def close_storage():
    """call the storage"""
    storage.close()


if __name__ == "__main__":
    # retrieve host and port environment variable
    host = getenv('HBNB_API_HOST', '0.0.0.0')
    port = getenv('HBNB_API_PORT', '5000')
    # run the flask application with threading enabled
    app.run(host=host, port=port, threaded=True)
