from flask import render_template, request
from yose import app
from prime_factor import is_an_int, is_too_big, is_too_small, decompose


@app.route("/primeFactors/ui")
def ui():
    return render_template('ui.jade')


@app.route("/primeFactors/result")
def ui_result():
    request_param = request.args.get('number')
    if not is_an_int(request_param):
        return render_template('result.jade', result=request_param + " is not a number")

    number = int(request_param)
    if is_too_big(number):
        return render_template('result.jade', result="too big number (>1e6)")
    if is_too_small(number):
        return render_template('result.jade', result=str(number) + " is not an integer > 1")

    decomposition = decompose(number)

    return render_template('result.jade', result=_build_result(number,decomposition))


def _build_result(number, decomposition):
    result = str(number) + " = "
    for index, d in enumerate(decomposition):
        result += str(d)
        if index is not (len(decomposition) - 1):
            result += " x "
    return result
