from flask import Flask, jsonify, request, Response, render_template

app = Flask(__name__)
app.debug = True
app.jinja_env.add_extension('pyjade.ext.jinja.PyJadeExtension')


@app.route("/")
def alive():
    return jsonify({'alive': True})


@app.route("/primeFactors")
def prime_factors():
    response = []
    requested_numbers = request.values.getlist('number')
    for requested_number in requested_numbers:
        print "NUMBER: " + requested_number
        if not requested_number.isdigit():
            response.append("{\"number\":\"" + requested_number + "\",\"error\":\"" + "not a number" + "\"}")
            continue

        number = int(requested_number)
        if number > 1000000:
            response.append("{\"number\":" + requested_number + ",\"error\":\"" + "too big number (>1e6)" + "\"}")
            continue

        decomposition = decompose(number)
        response.append("{\"number\":" + requested_number + ",\"decomposition\":" + str(decomposition) + "}")

    return build_response(response)


def decompose(number):
    primes = []
    for candidate in range(2, number + 1):
        while number % candidate == 0:
            primes.append(candidate)
            number /= candidate
    return primes


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


@app.route("/primeFactors/ui")
def ui():
    return render_template('ui.jade')


@app.route("/primeFactors/result")
def ui_result():
    request_param = request.args.get('number')
    if not is_an_int(request_param):
        return render_template('result.jade', result=request_param + " is not a number")

    number = int(request_param)
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
    except ValueError:
        return False

if __name__ == "__main__":
    app.run(host='0.0.0.0')