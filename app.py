from flask import Flask, jsonify, request, Response, render_template
import os


app = Flask(__name__)
app.debug = True
app.jinja_env.add_extension('pyjade.ext.jinja.PyJadeExtension')


@app.route("/")
def alive():
    return jsonify({'alive': True})


@app.route("/primeFactors")
def primeFactors():
    requestParam = request.args.get('number')
    if not requestParam.isdigit():
        return not_a_number_response(requestParam)

    number = int(requestParam)
    if number > 1000000:
        return too_big_number(number)
    decomposition = decompose(number)
    return build_response(decomposition, number)


def decompose(number):
    primes = []
    for candidate in range(2, number + 1):
        while number % candidate == 0:
            primes.append(candidate)
            number /= candidate
    return primes


def build_response(decomposition, number):
    hand_build_json = "{\"number\":" + str(number) + ",\"decomposition\":" + str(decomposition) + "}"
    response = Response(response=hand_build_json, status=200, mimetype="application/json")
    return response


def not_a_number_response(request):
    hand_build_json = "{\"number\":\"" + request + "\",\"error\":\"" + "not a number" + "\"}"
    response = Response(response=hand_build_json, status=200, mimetype="application/json")
    return response


def too_big_number(number):
    hand_build_json = "{\"number\":" + str(number) + ",\"error\":\"" + "too big number (>1e6)" + "\"}"
    response = Response(response=hand_build_json, status=200, mimetype="application/json")
    return response

@app.route("/primeFactors/ui")
def ui():
    return render_template('ui.jade')


@app.route("/primeFactors/result")
def ui_result():
    requestParam = request.args.get('number')
    if not is_an_int(requestParam):
        return render_template('result.jade', result=requestParam + " is not a number")

    number = int(requestParam)
    if number > 1000000:
        return render_template('result.jade', result="too big number (>1e6)")
    if number < 1:
        return render_template('result.jade', result=str(number) + " is not an integer > 1")
    decomposition = decompose(number)
    result = str(number) + " = "
    for index, d in enumerate(decomposition):
        result += str(d)
        if index is not (len(decomposition) - 1):
            result += " x "

    return render_template('result.jade', result=result)


def is_an_int(string):
    try:
        int(string)
        return True
    except:
        return False

if __name__ == "__main__":
    app.run(host='0.0.0.0')