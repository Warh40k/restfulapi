#!venv/bin/python
from flask import Flask, jsonify, abort, make_response, request

app = Flask(__name__)


promos = [
    {
        'id': 1,
        'name': u'Milk hatred',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol',
        'prizes': [
            {
                'id': 1,
                "description": "Milk-shake"
            },
            {
                'id': 2,
                'description': "Cookish"
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
                        "description": "Cookish"
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
    return jsonify(result)


@app.route('/promo/<int:promo_id>', methods=['GET'])
def get_promo(promo_id):
    promo = list(filter(lambda t: t['id'] == promo_id, promos))
    if len(promo) == 0:
        abort(404)
    return jsonify(promo)


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


@app.route('/promo/<int:promo_id>', methods=['DELETE'])
def delete_task(promo_id):
    promo = list(filter(lambda t: t['id'] == promo_id, promos))
    if len(promo) == 0:
        abort(404)
    promos.remove(promo[0])
    return jsonify({"Result": "True"})


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
    return jsonify({"result": "True"})


def get_promo_index(promo_id):
    for i in promos:
        if i['id'] == promo_id:
            return list(promos).index(i)

    abort(404)


@app.route('/promo/<int:promo_id>/prize/<int:prize_id>', methods=['DELETE'])
def delete_prize(prize_id, promo_id):
    promo = get_promo_index(promo_id)
    print(promo)
    prize = list(filter(lambda t: t['id'] == prize_id, promos[promo]['prizes']))
    if len(prize) == 0:
        abort(404)
    print(prize)
    promos[promo]["prizes"].remove(prize[0])

    return jsonify({"result": "True"})


if __name__ == '__main__':
    app.run(debug=True)
