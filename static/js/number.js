var $ = $ || require('jquery');

function Number() {
}

Number.prototype.decompose = function() {
	$.get('/primeFactors/result?number=' + $('#number').val())
		.success(this.displayResults);
};

Number.prototype.displayResults = function(data) {
    $('#result').text(data)
};

var module = module || {};
module.exports = Number;