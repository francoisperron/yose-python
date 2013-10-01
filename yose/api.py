from flask import jsonify, request, Response
from yose import app
from prime_factor import is_an_int, is_too_big, decompose


@app.route("/")
def alive():
    return jsonify({'alive': True})


@app.route("/primeFactors")
def prime_factors():
    response = []
    requested_numbers = request.values.getlist('number')
    for requested_number in requested_numbers:
        if not is_an_int(requested_number):
            response.append("{\"number\":\"" + requested_number + "\",\"error\":\"" + "not a number" + "\"}")
            continue

        number = int(requested_number)
        if is_too_big(number):
            response.append("{\"number\":" + requested_number + ",\"error\":\"" + "too big number (>1e6)" + "\"}")
            continue

        decomposition = decompose(number)
        response.append("{\"number\":" + requested_number + ",\"decomposition\":" + str(decomposition) + "}")

    return build_response(response)


def build_response(json):
    if len(json) == 1:
        hand_made_json = json
    else:
        hand_made_json = ["["]
        for index, response in enumerate(json):
            hand_made_json.append(response)
            if index is not (len(json) - 1):
                hand_made_json.append(",")
        hand_made_json.append("]")
    response = Response(response=hand_made_json, status=200, mimetype="application/json")
    return response