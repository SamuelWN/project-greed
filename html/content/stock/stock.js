function formatYahoo(data) {
	var quotes = data.query.results.quote.reverse();
	var chartData = {};

	for (var q in quotes) {
		var symbol = quotes[q].Symbol;
		var date = parseInt(new Date(quotes[q].Date).getTime());
		var close = parseFloat(quotes[q].Close);

		if (chartData[symbol] == null) {
			chartData[symbol] = [];
		}
		chartData[symbol].push([date, close]);
	}

	for (var c in chartData) {
		stockDetail_addchart(stockChart, c, chartData[c]);
	}
}

function Stock(symbol, company, currentValue) {
	this.symbol = symbol;
	this.company = company;
	this.currentValue = currentValue;

	var endDate = new Date();
	var startDate = new Date();
	startDate.setFullYear(endDate.getFullYear() - 1);
	var startDate_string = startDate.getFullYear() + "-" + (startDate.getMonth() + 1) + "-" + startDate.getDate();
	var endDate_string = endDate.getFullYear() + "-" + (endDate.getMonth() + 1) + "-" + endDate.getDate();

	var YQL_base = "http://query.yahooapis.com/v1/public/yql";
	var YQL_query = "SELECT Symbol, Date, Close " +
		"FROM yahoo.finance.historicaldata " +
		"WHERE symbol in ('" + symbol + "') " +
		"AND startDate = '" + startDate_string + "' " +
		"AND endDate = '" + endDate_string + "'";
	var YQL_format = "json";
	var YQL_callback = "formatYahoo";
	var YQL_env = "store://datatables.org/alltableswithkeys";

	this.YQL = function () {
		return YQL_base +
		"?q=" + YQL_query +
		"&format=" + YQL_format +
		"&env=" + YQL_env +
		"&callback=" + YQL_callback;
	};

	this.history = function (renderTarget) {
		var xmlhttp = new XMLHttpRequest();

		//stockSummary_highcharts(myStock.YQL(), renderTarget);
	};
}

function StockHistorical(unixtime, value) {
	this.unixtime = unixtime;
	this.value = value;

	var date = new Date();
	date.setTime(unixtime * 1000);

	this.getTime = function () {
		return date.getTime();
	}

	this.dateString = function () {
		return (date.getMonth() + 1) + "/" + (date.getDate()) + "/" + (date.getFullYear());
	}
}

function stockTitle_span(stock) {
	//var span = document.createElement("span");
	return document.createTextNode(stock.symbol + " - " + stock.company);
	//return span;
}

function stockDetail_basechart(renderTarget) {
	return new Highcharts.StockChart({
		chart : {
			renderTo : renderTarget
		},
		rangeSelector : {
			enabled : true
		},
		xAxis : {
			ordinal : false
		}
	});
}

function stockDetail_addchart(chart, dataName, dataTarget) {
	chart.addSeries({
		name : dataName,
		data : dataTarget,
	});
}

function stockSummary_highcharts(dataName, dataTarget, renderTarget) {
	var chart = new Highcharts.StockChart({
			chart : {
				renderTo : renderTarget
			},
			rangeSelector : {
				enabled : true
			}
		});
	chart.addSeries({
		name : dataName,
		data : dataTarget,
	});
}

//name, valueTotal, valueCash, valueStock, valueComp
function stockSummary_dl(stock) {
	var dl = document.createElement("dl");

	return dl;
}

Element.prototype.build_stockTitle = function (stock) {
	this.appendChild(stockTitle_span(stock));
}

Element.prototype.build_stockSummary = function (stock) {
	this.appendChild(stockSummary_dl(stock));
}

Element.prototype.build_stockDetail = function (stock) {
	var script = document.createElement('script');
	script.src = stock.YQL();
	this.appendChild(script);

	div = document.createElement("div");
	this.appendChild(div);

	stockChart = stockDetail_basechart(div);
}
var stockChart;

// TODO: make this apply to actual stock
var myStock = new Stock("MSFT", "Microsoft Corporation", 500);

document.getElementById("title").build_stockTitle(myStock);
document.getElementById("summary").build_stockSummary(myStock);
document.getElementById("detail").build_stockDetail(myStock);
