#!venv/bin/python
from flask import Flask, jsonify, abort, make_response, request
import random
app = Flask(__name__)


promos = [
    {
        'id': 1,
        'name': u'Milk contest',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol',
        'prizes': [
            {
                'id': 1,
                "description": "Milk-shake"
            },
            {
                'id': 2,
                'description': "Cheese"
            }
        ],
        "participants": [
            {
                "id":1,
                "name":"Anton"
            },
            {
                "id":2,
                "name":"Pavel"
            }
        ],
        "raffle": [
            {
                "winner":
                {
                    "id": 2,
                    "name": "Pavel"
                },
                "prize":
                {
                    "id": 1,
                    "description": "Milkshake"
                }
            },

            {
                "winner":
                    {
                        "id": 1,
                        "name": "Anton"
                    },
                "prize":
                    {
                        "id": 2,
                        "description": "Cheese"
                    }
            }
        ],
    },
    {
        'id': 2,
        'name': u'Make repost - get outpost',
        'description': u'Won a outpost in out random selection promo',
        "participants": [
            {
                "id": 1,
                "name": "Anton"
            },
            {
                "id": 2,
                "name": "Pavel"
            },
        ]
    },
]


@app.route('/promo', methods=['GET'])
def get_promos():
    result = []
    for i in promos:
        result.append(
        {
            'description': i['name'],
            'name': i['description']
        })
    print(result)
    return jsonify(result), 200


@app.route('/promo/<int:promo_id>', methods=['GET'])
def get_promo(promo_id):
    promo = list(filter(lambda t: t['id'] == promo_id, promos))
    if len(promo) == 0:
        abort(404)
    return jsonify(promo), 200


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.route('/promo', methods=['POST'])
def create_promo():
    if not request.json or not 'name' in request.json:
        abort(400)
    promo = {
        'id': promos[-1]['id'] + 1,
        'name': request.json['name'],
        'description': request.json.get('description', ""),
    }
    promos.append(promo)
    return jsonify(promo), 201


@app.route('/promo/<int:promo_id>/participant', methods=['POST'])
def create_participant(promo_id):
    if not request.json or not 'name' in request.json:
        abort(400)
    promo = get_promo_index(promo_id)
    print(promos[promo]["participants"])
    participant = {
        'id': promos[promo]["participants"][-1]["id"] + 1,
        'name': request.json['name']
    }
    promos[promo]["participants"].append(participant)
    print(promos[promo]["participants"])
    return jsonify(participant), 201


@app.route('/promo/<int:promo_id>/prize', methods=['POST'])
def create_prize(promo_id):
    if not request.json or not 'description' in request.json:
        abort(400)
    promo = get_promo_index(promo_id)
    print(promos[promo]["prizes"])
    prize = {
        'id': promos[promo]["prizes"][-1]["id"] + 1,
        'description': request.json['description']
    }
    promos[promo]["prizes"].append(prize)
    print(promos[promo]["prizes"])
    return jsonify(prize), 201

"""
@app.route('/promo/<int:promo_id>/raffle', methods=['POST'])
def make_raffle(promo_id):
    promo = get_promo_index(promo_id)
    print(promos[promo]["prizes"])
    if len(promos[promo]["participants"]) != len(promos[promo]["prizes"]):
        abort(400)
    participants = promos[promo]["participants"]
    print(type(participants))
    random.shuffle(participants)
    print(participants)
    raffle=[]
    for i in range(participants):
    raffle =[
        {
        "winner": {
            "id": participants[0]['id'],
            "name": participants[0]['name']
            },
        "prize":
            {
            'id': promos[promo]["prizes"][0]["id"],
            'description':promos[promo]["prizes"][0]["id"]
            }
        }

    ]
    prize = {
        'id': promos[promo]["prizes"][-1]["id"] + 1,
        'description': request.json['description']
    }
    promos[promo]["prizes"].append(prize)
    print(promos[promo]["prizes"])
    return jsonify(prize), 201
"""


@app.route('/promo/<int:promo_id>', methods=['PUT'])
def update_task(promo_id):
    promo_ind = get_promo_index(promo_id)
    if promo_ind is None:
        abort(404)
    if not request.json:
        abort(400)
    if request.json.get('name', promos[promo_ind]['name']) != "":
        promos[promo_ind]['name'] = request.json.get('name', promos[promo_ind]['name'])
    else:
        abort(400)
    promos[promo_ind]['description'] = request.json.get('description', promos[promo_ind]['description'])
    return jsonify(promos[promo_ind]), 201


@app.route('/promo/<int:promo_id>', methods=['DELETE'])
def delete_task(promo_id):
    promo = list(filter(lambda t: t['id'] == promo_id, promos))
    if len(promo) == 0:
        abort(404)
    promos.remove(promo[0])
    return jsonify({"Result": "True"}), 200


@app.route('/promo/<int:promo_id>/participant/<int:participant_id>', methods=['DELETE'])
def delete_participant(participant_id, promo_id):
    promo = get_promo_index(promo_id)
    print(promo)
    participant = list(filter(lambda t: t['id'] == participant_id, promos[promo]['participants']))
    if len(participant) == 0:
        abort(404)
    print(participant)
    promos[promo]["participants"].remove(participant[0])
    print(promos[promo]["participants"])
    return jsonify({"result": "True"}), 200


def get_promo_index(promo_id):
    for i in promos:
        if i['id'] == promo_id:
            return list(promos).index(i)

    abort(400)


@app.route('/promo/<int:promo_id>/prize/<int:prize_id>', methods=['DELETE'])
def delete_prize(prize_id, promo_id):
    promo = get_promo_index(promo_id)
    print(promo)
    prize = list(filter(lambda t: t['id'] == prize_id, promos[promo]['prizes']))
    if len(prize) == 0:
        abort(404)
    print(prize)
    promos[promo]["prizes"].remove(prize[0])

    return jsonify({"result": "True"}), 200


if __name__ == '__main__':
    app.run(debug=True)
