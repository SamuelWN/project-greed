function formatYahoo(data) {
	var quotes = data.query.results.quote.reverse();
	var stockValues = {};
	for (var q in quotes) {
		var symbol = quotes[q].Symbol;
		var date = parseInt(new Date(quotes[q].Date).getTime());
		var close = parseFloat(quotes[q].Close);
		if (stockValues[symbol] == null) {
			stockValues[symbol] = {};
		}
		stockValues[symbol][date] = close;
	}
	populateHistory(myPortfolio.listHistory, stockValues);
}

var whatif_symbol;
var whatif_count;
var whatif_unixtime;
function formatYahooWI(data) {
	var quotes = data.query.results.quote.reverse();
	var stockValues = {};
	for (var q in quotes) {
		var symbol = quotes[q].Symbol;
		var date = parseInt(new Date(quotes[q].Date).getTime());
		var close = parseFloat(quotes[q].Close);
		if (stockValues[symbol] == null) {
			stockValues[symbol] = {};
		}
		stockValues[symbol][date] = close;
	}
	populateWhatif(whatif_symbol, whatif_count, whatif_unixtime, stockValues);
}

function Portfolio(name, valueCash, valueStock, valueComp, compEntryFee, listStock, listHistory) {
	this.name = name;
	this.valueCash = valueCash;
	this.valueStock = valueStock;
	this.valueComp = valueComp;
	this.compEntryFee = typeof compEntryFee !== 'undefined' ? compEntryFee : undefined;
	this.listStock = listStock;
	this.listHistory = listHistory;

	this.valueTotal = this.valueCash + this.valueStock + this.valueComp;

	var symbols = [];
	for (var s in listStock) {
		symbols.push("'" + listStock[s].symbol + "'");
	}
	var symbols_string = symbols.join(",");

	var endDate = new Date();
	var startDate = new Date();
	startDate.setTime(listHistory[0].unixtime * 1000);
	startDate.setDate(startDate.getDate() - 3);
	var startDate_string = startDate.getFullYear() + "-" + (startDate.getMonth() + 1) + "-" + startDate.getDate();
	var endDate_string = endDate.getFullYear() + "-" + (endDate.getMonth() + 1) + "-" + endDate.getDate();

	var callback = "formatYahoo";

	var YQL_base = "http://query.yahooapis.com/v1/public/yql";
	var YQL_query = "SELECT Symbol, Date, Close " +
		"FROM yahoo.finance.historicaldata " +
		"WHERE symbol in (" + symbols_string + ") " +
		"AND startDate = '" + startDate_string + "' " +
		"AND endDate = '" + endDate_string + "'";
	var YQL_format = "json";
	var YQL_callback = callback;
	var YQL_env = "store://datatables.org/alltableswithkeys";

	this.YQL = function () {
		return YQL_base +
		"?q=" + YQL_query +
		"&format=" + YQL_format +
		"&env=" + YQL_env +
		"&callback=" + YQL_callback;
	};
}

function portfolioInfo_basechart(renderTarget, dataTarget, stockCount) {
	var dataSum = 0;
	for (var d in dataTarget) {
		var symbol = dataTarget[d].symbol;
		var value = dataTarget[d].current_value;
		var count = stockCount[symbol]
			var totalValue = value * count
			dataTarget[d].y = totalValue;
		dataTarget[d].name = symbol;
		dataSum += totalValue;
	}
	var chart = new Highcharts.Chart({
			chart : {
				renderTo : renderTarget,
			},
			title : {
				text : "Stock Value: " + "$" + Highcharts.numberFormat(dataSum, 2)
			},
			subtitle : {
				text : Highcharts.dateFormat("%A, %B %e, %Y, at %l:%M:%S%P", new Date().getTime())
			},
			tooltip : {
				headerFormat : '<span style="font-size: 10px">{point.key}</span><br/>',
				pointFormat : '<b>${point.y:.2f}</b>'
			},
			plotOptions : {
				pie : {
					dataLabels : {
						formatter : function () {
							if (this.y > 0) {
								return this.point.company;
							}
						}
					},
				}
			}
		});
	chart.addSeries({
		type : "pie",
		name : "value",
		data : dataTarget
	});
	return chart;
}

function portfolioInfo_setchart(chart, dataName, dataTarget, dataTotal, dataTime) {
	chart.setTitle({
		text : "Stock Value: " + "$" + Highcharts.numberFormat(dataTotal, 2)
	}, {
		text : Highcharts.dateFormat("%A, %B %e, %Y, at %l:%M:%S%P", dataTime)
	});
	for (s in chart.series) {
		if (chart.series[s].name == dataName) {
			return chart.series[s].setData(dataTarget);
		}
	}
}

function portfolioHistory_basechart(renderTarget) {
	return new Highcharts.StockChart({
		chart : {
			renderTo : renderTarget
		},
		legend : {
			enabled : true,
		},
		plotOptions : {
			areaspline : {
				fillOpacity : 1,
				stacking : 'normal',
				trackByArea : true,
				point : {
					events : {
						click : function (e) {
							var seriesArray = this.series.chart.series
								for (var s in seriesArray) {
									if (seriesArray[s].name == "stock") {
										newThis = seriesArray[s].data[this.index];
										portfolioInfo_setchart(infoChart, "value", newThis.stocks, newThis.y, newThis.x);
									}
								}
						}
					}
				}
			}
		},
		tooltip : {
			/*
			headerFormat: '<span style="font-size: 10px">{point.key}</span><br/>',
			pointFormat: '<span style="color:{series.color}">\u25CF</span> {series.name}: <b>${point.y:.2f}</b>, {point.total}<br/>',
			 */
			formatter : function () {
				var format = document.createElement("div");

				var date = document.createElement("div");
				date.appendChild(document.createTextNode(Highcharts.dateFormat("%a %m/%d/%y at %H:%M:%S", this.points[0].x)));
				date.appendChild(document.createElement("br"));
				date.style.fontSize = "x-small";

				var totalValue = document.createElement("div");
				totalValue.appendChild(document.createTextNode("$" + Highcharts.numberFormat(this.points[0].total, 2)));
				totalValue.appendChild(document.createElement("br"));
				totalValue.style.fontSize = "large";
				totalValue.style.fontWeight = "bold";

				var values = document.createElement("div");

				format.appendChild(date);
				format.appendChild(totalValue);
				format.appendChild(values);

				for (s in this.points) {
					if (this.points[s].series.name != "whatif") {
						var point = document.createElement("div");

						var bullet = document.createElement("span");
						bullet.appendChild(document.createTextNode("\u25CF  "));
						bullet.style.color = this.points[s].series.color;

						var name = document.createElement("span");
						name.appendChild(document.createTextNode(this.points[s].series.name));
						name.appendChild(document.createTextNode(":  "));

						var value = document.createElement("span");
						value.appendChild(document.createTextNode("$" + Highcharts.numberFormat(this.points[s].y, 2)));
						value.style.fontWeight = "bold";

						point.appendChild(bullet);
						point.appendChild(name);
						point.appendChild(value);
						point.appendChild(document.createElement("br"));

						values.appendChild(point);
					}

				}
				return format.innerHTML;
			},
		},
		series : {
			showInLegend : false,
		},
		rangeSelector : {
			enabled : true
		},
		xAxis : {
			ordinal : false
		},
		yAxis : {
			floor : 0,
		}
	});
}

function portfolioHistory_addchart(chart, dataName, dataTarget, dataIndex, isWhatIf) {
	return chart.addSeries({
		name : dataName,
		data : dataTarget,
		type : 'areaspline',
		index : dataIndex,
		cursor : "pointer",
		showInLegend : false,
	});
}

function populateHistory(portfolioHistory, stockValues) {
	historyChart.reflow();

	var chartData = {};
	chartData["cash"] = [];
	chartData["comp"] = [];
	chartData["stock"] = [];
	chartData["whatif"] = [];

	var stocksSorted = [];
	for (s in stockValues) {
		if (stockValues.hasOwnProperty(s)) {
			stocksSorted.push(s);
		}
	}
	stocksSorted.sort();

	for (var h in portfolioHistory) {
		var date = portfolioHistory[h].unixtime * 1000;
		var valueCash = portfolioHistory[h].cash_value;
		var valueComp = portfolioHistory[h].comp_value;
		var countStocks = portfolioHistory[h].stock_count;

		chartData["cash"].push([date, valueCash]);
		chartData["comp"].push([date, valueComp]);

		chartData["whatif"].push([date, 0]);

		var valueStockSum = 0;
		var valueStocks = [];

		for (var ss in stocksSorted) {
			var s = stocksSorted[ss];
			var count = countStocks[s];
			var value = getStockValue(s, date / 1000, stockValues);

			var valueStock = count * value || 0;
			valueStockSum += valueStock;
			valueStocks.push({
				"name" : s,
				"y" : valueStock,
				"count" : count,
				"value" : value
			});
		}
		chartData["stock"].push({
			"x" : date,
			"y" : valueStockSum,
			"stocks" : valueStocks
		});
	}

	var whatifSeries = portfolioHistory_addchart(historyChart, "whatif", chartData["whatif"], 4);
	var stockSeries = portfolioHistory_addchart(historyChart, "stock", chartData["stock"], 1);
	var compSeries = portfolioHistory_addchart(historyChart, "comp", chartData["comp"], 2);
	var cashSeries = portfolioHistory_addchart(historyChart, "cash", chartData["cash"], 3);
}

function populateWhatif(symbol, count, unixtime, stockValues) {
	var chartData = [];

	var historyDates = historyChart.series[0].xData;
	var historyValues = historyChart.series[0].stackedYData;

	var initialOffset = getStockValue(symbol, unixtime, stockValues) * count;
	chartData.push({
		"x" : unixtime * 1000,
		"y" : 0,
		"offsetStocks" : initialOffset,
		"offsetCash" : -1 * initialOffset
	});

	for (var h in historyDates) {
		var date = historyDates[h] / 1000;
		if (date > unixtime) {
			var value = historyValues[h];
			var offset = getStockValue(symbol, date, stockValues) * count;

			chartData.push({
				"x" : date * 1000,
				"y" : offset - initialOffset,
				"offsetStocks" : offset,
				"offsetCash" : -1 * initialOffset
			});
		}
	}
	for (s in historyChart.series) {
		if (historyChart.series[s].name == "whatif") {
			historyChart.series[s].setData(chartData);
			historyChart.series[s].update({
				showInLegend : true
			});
		}
	}
}

function whatif(e, wiSymbol, wiCount, wiUnixtime) {
	whatif_symbol = wiSymbol;
	whatif_count = wiCount;
	whatif_unixtime = wiUnixtime;

	symbols_string = "'" + wiSymbol + "'";

	var endDate = new Date();
	var startDate = new Date();
	startDate.setTime(wiUnixtime * 1000);
	startDate.setDate(startDate.getDate() - 3);
	var startDate_string = startDate.getFullYear() + "-" + (startDate.getMonth() + 1) + "-" + startDate.getDate();
	var endDate_string = endDate.getFullYear() + "-" + (endDate.getMonth() + 1) + "-" + endDate.getDate();

	var callback = "formatYahooWI";

	var YQL_base = "http://query.yahooapis.com/v1/public/yql";
	var YQL_query = "SELECT Symbol, Date, Close " +
		"FROM yahoo.finance.historicaldata " +
		"WHERE symbol in (" + symbols_string + ") " +
		"AND startDate = '" + startDate_string + "' " +
		"AND endDate = '" + endDate_string + "'";
	var YQL_format = "json";
	var YQL_callback = callback;
	var YQL_env = "store://datatables.org/alltableswithkeys";
	YQL = function () {
		return YQL_base +
		"?q=" + YQL_query +
		"&format=" + YQL_format +
		"&env=" + YQL_env +
		"&callback=" + YQL_callback
	};

	//console.log(YQL());

	var script = document.createElement('script');
	script.src = YQL();
	e.appendChild(script);
}

function getStockValue(stock, unixtime, stockValues) {
	var values = Object.keys(stockValues[stock]);
	unixtime = unixtime * 1000;

	var bestValue = 0;
	for (var v in values) {
		if (values[v] >= unixtime) {
			if (values[v] == unixtime) {
				bestValue = stockValues[stock][values[v]];
			}
			break;
		}
		if (values[v] < unixtime) {
			bestValue = stockValues[stock][values[v]];
		}
	}
	return bestValue;
}

function portfolioTable_tr_th() {
	var tr = document.createElement("tr");

	var th_company = document.createElement("th");
	th_company.className = "company";
	th_company.appendChild(document.createTextNode("Company"));

	var th_symbol = document.createElement("th");
	th_symbol.appendChild(document.createTextNode("Stock"));

	var th_valueTotal = document.createElement("th");
	th_valueTotal.appendChild(document.createTextNode("Total Value"));

	var th_count = document.createElement("th");
	th_count.appendChild(document.createTextNode("Shares"));

	var th_value = document.createElement("th");
	th_value.appendChild(document.createTextNode("Value"));

	tr.appendChild(th_company);
	tr.appendChild(th_symbol);
	tr.appendChild(th_valueTotal);
	tr.appendChild(th_count);
	tr.appendChild(th_value);

	return tr;
}

function portfolioTable_td_buysell() {
	var td = document.createElement("td");

	var input_number = document.createElement("input");
	input_number.setAttribute("type", "number");
	input_number.setAttribute("min", "0");
	input_number.setAttribute("max", "9999");
	input_number.setAttribute("maxlength", "5");
	input_number.setAttribute("placeholder", "0");

	var input_buy = document.createElement("input");
	input_buy.setAttribute("type", "button");
	input_buy.setAttribute("value", "Buy");

	var input_sell = document.createElement("input");
	input_sell.setAttribute("type", "button");
	input_sell.setAttribute("value", "Sell");

	td.appendChild(input_number);
	td.appendChild(input_buy);
	td.appendChild(input_sell);

	return td;
}

function portfolioTable_tr_td(stock, count) {
	var symbol = stock.symbol;
	var company = stock.company;
	var value = stock.current_value;
	var count = count;
	var valueTotal = value * count;

	var tr = document.createElement("tr");

	var td_company = document.createElement("td");
	td_company.className = "company";
	td_company.appendChild(document.createTextNode(company));

	var td_symbol = document.createElement("td");
	td_symbol.appendChild(document.createTextNode(symbol));

	var td_valueTotal = document.createElement("td");
	td_valueTotal.className = "dollars";
	td_valueTotal.appendChild(document.createTextNode(valueTotal));

	var td_count = document.createElement("td");
	td_count.appendChild(document.createTextNode(count));

	var td_value = document.createElement("td");
	td_value.className = "dollars";
	td_value.appendChild(document.createTextNode(value));

	tr.appendChild(td_company);
	tr.appendChild(td_symbol);
	tr.appendChild(td_valueTotal);
	tr.appendChild(td_count);
	tr.appendChild(td_value);
	tr.appendChild(portfolioTable_td_buysell());

	return tr;
}

function portfolioTable_table(portfolio) {
	var table = document.createElement("table");
	table.appendChild(portfolioTable_tr_th());
	for (var s in portfolio.listStock) {
		var stock = portfolio.listStock[s];
		var count = portfolio.listHistory.slice(-1)[0].stock_count[stock.symbol];

		table.appendChild(portfolioTable_tr_td(stock, count));
	}
	return table;
}

function portfolioTitle_span(portfolio) {
	return document.createTextNode(portfolio.name);
}

function portfolioSummary_dl(portfolio) {
	var dl = document.createElement("dl");

	var dt_total = document.createElement("dt");
	dt_total.appendChild(document.createTextNode("Total Value"));
	var dd_total = document.createElement("dd");
	dd_total.className = "dollars";
	dd_total.appendChild(document.createTextNode(portfolio.valueTotal));

	var dt_cash = document.createElement("dt");
	dt_cash.appendChild(document.createTextNode("Cash"));
	var dd_cash = document.createElement("dd");
	dd_cash.className = "dollars";
	dd_cash.appendChild(document.createTextNode(portfolio.valueCash));

	var dt_stock = document.createElement("dt");
	dt_stock.appendChild(document.createTextNode("Stock Value"));
	var dd_stock = document.createElement("dd");
	dd_stock.className = "dollars";
	dd_stock.appendChild(document.createTextNode(portfolio.valueStock));

	var dt_comp = document.createElement("dt");
	dt_comp.appendChild(document.createTextNode("Competition Value"));
	var dd_comp = document.createElement("dd");
	dd_comp.className = "dollars";
	dd_comp.appendChild(document.createTextNode(portfolio.valueComp));

	dl.appendChild(dt_total);
	dl.appendChild(dd_total);
	dl.appendChild(dt_cash);
	dl.appendChild(dd_cash);
	dl.appendChild(dt_stock);
	dl.appendChild(dd_stock);
	dl.appendChild(dt_comp);
	dl.appendChild(dd_comp);

	var info_chart = document.createElement("div");
	dl.appendChild(info_chart);

	var history_chart = document.createElement("div");
	dl.appendChild(history_chart);

	infoChart = portfolioInfo_basechart(info_chart, portfolio.listStock, portfolio.listHistory.slice(-1)[0].stock_count);
	historyChart = portfolioHistory_basechart(history_chart);

	return dl;
}

var historyChart;
var infoChart;

function portfolioSummary_whatif() {
	var div = document.createElement("div");

	var input_symbol = document.createElement("input");
	input_symbol.type = "text";
	input_symbol.pattern = "[A-Z]{1,5}";
	input_symbol.maxlength = 5;
	input_symbol.size = 3;
	input_symbol.placeholder = "symbol";

	var input_number = document.createElement("input");
	input_number.type = "number";
	input_number.min = 0;
	input_number.max = 9999;
	input_number.maxlength = 4;
	input_number.placeholder = 0;

	// CHROME ONLY
	/*
	var input_datetime = document.createElement("input");
	input_datetime.type = "time";
	input_datetime.setAttribute("size", "1");
	 */

	var currentDatetime = new Date();
	var currentYear = currentDatetime.getFullYear();
	var currentMonth = currentDatetime.getMonth() + 1;
	var currentDay = currentDatetime.getDate();

	var input_datetime = document.createElement("span");

	var input_datetime_year = document.createElement("input");
	input_datetime_year.type = "number";
	input_datetime_year.min = 1970;
	input_datetime_year.max = 2037;
	input_datetime_year.maxlength = 4;
	input_datetime_year.placeholder = currentYear;
	input_datetime_year.defaultValue = currentYear;

	var input_datetime_month = document.createElement("input");
	input_datetime_month.type = "number";
	input_datetime_month.min = 1;
	input_datetime_month.max = 12;
	input_datetime_month.maxlength = 2;
	input_datetime_month.placeholder = currentMonth;
	input_datetime_month.defaultValue = currentMonth;

	var input_datetime_day = document.createElement("input");
	input_datetime_day.type = "number";
	input_datetime_day.min = 1;
	input_datetime_day.max = 31;
	input_datetime_day.maxlength = 2;
	input_datetime_day.placeholder = currentDay;
	input_datetime_day.defaultValue = currentDay;

	input_datetime.appendChild(input_datetime_month);
	input_datetime.appendChild(input_datetime_day);
	input_datetime.appendChild(input_datetime_year);

	var input_submit = document.createElement("input");
	input_submit.type = "button";
	input_submit.value = "What If...";
	input_submit.onclick = function () {
		var symbol = input_symbol.value;
		var count = input_number.value;

		var datetime_year = input_datetime_year.value;
		var datetime_month = input_datetime_month.value;
		var datetime_day = input_datetime_day.value;

		var inputDatetime = new Date(datetime_year, datetime_month - 1, datetime_day);

		whatif(div, symbol, count, inputDatetime.getTime() / 1000);
	};

	div.appendChild(input_symbol);
	div.appendChild(input_number);
	div.appendChild(input_datetime);

	div.appendChild(input_datetime_year);

	div.appendChild(input_submit);

	return div;
}

Element.prototype.build_portfolioTitle = function (portfolio) {
	this.appendChild(portfolioTitle_span(portfolio));
}

Element.prototype.build_portfolioSummary = function (portfolio) {
	this.appendChild(portfolioSummary_dl(portfolio));

	this.appendChild(portfolioSummary_whatif());

	var script = document.createElement('script');
	script.src = myPortfolio.YQL();
	this.appendChild(script);
}

Element.prototype.build_portfolioTable = function (portfolio) {
	this.appendChild(portfolioTable_table(portfolio));
}

// TODO: make this apply to actual stocks
var myPortfolioStocks = [{
		"symbol" : "AAPL",
		"company" : "Apple Inc.",
		"current_value" : 95.00
	}, {
		"symbol" : "GOOG",
		"company" : "Google Inc.",
		"current_value" : 100.00
	},
];

// TODO: make this apply to actual portfolio histories
var myPortfolioHistory = [{
		"unixtime" : 1417805000,
		"cash_value" : 9925.00,
		"comp_value" : 0.00,
		"stock_count" : {
			"AAPL" : 0,
			"GOOG" : 1
		}
	}, {
		"unixtime" : 1417805053,
		"cash_value" : 9525.00,
		"comp_value" : 0.00,
		"stock_count" : {
			"AAPL" : 0,
			"GOOG" : 1
		}
	}, {
		"unixtime" : 1417891550,
		"cash_value" : 9230.00,
		"comp_value" : 400.00,
		"stock_count" : {
			"AAPL" : 1,
			"GOOG" : 5
		}
	}, {
		"unixtime" : 1417891551,
		"cash_value" : 9140.00,
		"comp_value" : 400.00,
		"stock_count" : {
			"AAPL" : 1,
			"GOOG" : 6
		}
	}, {
		"unixtime" : 1417891552,
		"cash_value" : 9220.00,
		"comp_value" : 400.00,
		"stock_count" : {
			"AAPL" : 0,
			"GOOG" : 6
		}
	}, {
		"unixtime" : 1417891553,
		"cash_value" : 9320.00,
		"comp_value" : 400.00,
		"stock_count" : {
			"AAPL" : 0,
			"GOOG" : 4
		}
	}, {
		"unixtime" : 1417891556,
		"cash_value" : 9270.00,
		"comp_value" : 500.00,
		"stock_count" : {
			"AAPL" : 0,
			"GOOG" : 4
		}
	}, {
		"unixtime" : 1417977953,
		"cash_value" : 9170.00,
		"comp_value" : 550.00,
		"stock_count" : {
			"AAPL" : 0,
			"GOOG" : 4
		}
	}, {
		"unixtime" : 1417977956,
		"cash_value" : 9220.00,
		"comp_value" : 650.00,
		"stock_count" : {
			"AAPL" : 0,
			"GOOG" : 4
		}
	}, {
		"unixtime" : 1418064353,
		"cash_value" : 9820.00,
		"comp_value" : 600.00,
		"stock_count" : {
			"AAPL" : 0,
			"GOOG" : 4
		}
	}, {
		"unixtime" : 1418288845,
		"cash_value" : 9595.00,
		"comp_value" : 0.00,
		"stock_count" : {
			"AAPL" : 3,
			"GOOG" : 4
		}
	},
];

// TODO: make this apply to actual portfolios
var myPortfolio = new Portfolio("Portfolio1", 5000, 7500, 0, null, myPortfolioStocks, myPortfolioHistory);

document.getElementById("title").build_portfolioTitle(myPortfolio);
document.getElementById("summary").build_portfolioSummary(myPortfolio);
document.getElementById("detail").build_portfolioTable(myPortfolio);
