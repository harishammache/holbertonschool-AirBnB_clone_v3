#!/usr/bin/python3
"""
    Create a new view for State objects that handles
    all default RESTFul API actions
"""


from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def states():
    """Retrieve a list of all State objects"""
    states = storage.all(State) # recupère tous les objets de type State
    state_list = [] # cree une liste vide
    for state in states.values(): 
        # convertie en dictionnaire qui est ajouté a la liste
        state_list.append(state.to_dict())
    return jsonify(state_list) # return la list convertie en dictionnaire json


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_states(state_id):
    """Retrieve a State object by ID"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404) # Abandonne la requête avec une erreur 404
    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'], strict_slashes=False)
def delete_state(state_id):
    """Delete a State object by ID"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    
    # Supprimer l'objet State de la base de données
    storage.delete(state)
    storage.save()

    return {}, 200 # retourne un dictionnaire vide et un code 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """Create a new State"""
    if not request.is_json:
        abort(400, 'Not a JSON')
    data = request.get_json()

    if 'name' not in data:
        abort(400, 'Missing name')

    new_state = State(name=data['name'])
    storage.new(new_state)
    storage.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """Update a State object."""
    state = storage.get(State, state_id)
    if not state:
        abort(404)

    data = request.get_json(silent=True)
    if data is None:
        abort(400, "Not a JSON")

    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(state, key, value)

    storage.save()
    return jsonify(state.to_dict()), 200
