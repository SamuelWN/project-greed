var chartOptions = {
	animation: false,
	
	segmentShowStroke : true,
	segmentStrokeColor : "black",
	segmentStrokeWidth : 2,
	
	showTooltips: true,
	tooltipTemplate: "<%if (label){%><%=label%>: $<%}%><%= value %>",
};

function Portfolio(name, valueCash, valueStock, valueComp, compEntryFee, listStock, listHistory) {
	this.name = name;
	this.valueCash = valueCash;
	this.valueStock = valueStock;
	this.valueComp = valueComp;
	this.compEntryFee = typeof compEntryFee !== 'undefined' ? compEntryFee : undefined;
	this.listStock = listStock;
	this.listHistory = listHistory;
	
	this.valueTotal = this.valueCash + this.valueStock + this.valueComp;
}

function PortfolioHistorical(unixtime, valueCash, valueComp, countStocks) {
	this.unixtime = unixtime;
	this.valueCash = valueCash;
	this.valueComp = valueComp;
	this.countStocks = countStocks;
}

function PortfolioStock(symbol, company, value, count) {
	this.symbol = symbol;
	this.company = company;
	this.value = value;
	this.count = count;
	
	this.y = value;
	this.name = symbol;
	
	/*
	this.y = function() {
		return this.value;
	}
	this.name = function() {
		return this.symbol;
	}
	*/
}


/*
<tr>
	<th class="company">Company</th>
	<th>Stock</th>
	<th>Total Value</th>
	<th>Value</th>
	<th>Shares</th>
</tr>
*/
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


/*
<td>
	<input type="number" min=1>
	<button>Buy</button>
	<button>Sell</button>
</td>
*/
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
	//input_buy.onclick = function() {portfolioHistory_addchart(historyChart, "derp", [[1416805000 * 1000, -1000], [1417977953 * 1000, -1500], [1418805000 * 1000, -2000]])}
	input_buy.setAttribute("value", "Buy");
	
	var input_sell = document.createElement("input");
	input_sell.setAttribute("type", "submit");
	input_sell.appendChild(document.createTextNode("Sell"));
	
	td.appendChild(input_number);
	td.appendChild(input_buy);
	td.appendChild(input_sell);
	
	return td;
}


/*
<tr>
	<td class="company">Apple Inc.</td>
	<td>AAPL</td>
	<td class="dollars">115.47</td>
	<td>16</td>
	<td class="dollars">1847.52</td>
	[buysell]
</tr>
*/
function portfolioTable_tr_td(portfolioStock) {
	var tr = document.createElement("tr");
	
	var td_company = document.createElement("td");
	td_company.className = "company";
	td_company.appendChild(document.createTextNode(portfolioStock.company));
	
	var td_symbol = document.createElement("td");
	td_symbol.appendChild(document.createTextNode(portfolioStock.symbol));
	
	var td_valueTotal = document.createElement("td");
	td_valueTotal.className = "dollars";
	td_valueTotal.appendChild(document.createTextNode(portfolioStock.valueTotal));
	
	var td_count = document.createElement("td");
	td_count.appendChild(document.createTextNode(portfolioStock.count));
	
	var td_value = document.createElement("td");
	td_value.className = "dollars";
	td_value.appendChild(document.createTextNode(portfolioStock.value));
	
	tr.appendChild(td_company);
	tr.appendChild(td_symbol);
	tr.appendChild(td_valueTotal);
	tr.appendChild(td_count);
	tr.appendChild(td_value);
	tr.appendChild(portfolioTable_td_buysell());
	
	return tr;
}


function portfolioTable_table(portfolioStockList) {
	var table = document.createElement("table");
	table.appendChild(portfolioTable_tr_th());
	for (var portfolioStock in portfolioStockList) {
		table.appendChild(portfolioTable_tr_td(portfolioStockList[portfolioStock]));
	}
	return table;
}


function portfolioTitle_span(portfolio) {
	var span = document.createElement("span");
	span.appendChild(document.createTextNode(portfolio.name));
	return span;
}



//name, valueTotal, valueCash, valueStock, valueComp
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
	
	infoChart = portfolioInfo_basechart(info_chart, portfolio.listStock);
	historyChart = portfolioHistory_basechart(history_chart);
	
	return dl;
}

var historyChart;
var infoChart;




Element.prototype.build_portfolioTitle = function(portfolio) {
	this.appendChild(portfolioTitle_span(portfolio));
	
}

Element.prototype.build_portfolioSummary = function(portfolio) {
	this.appendChild(portfolioSummary_dl(portfolio));
}

Element.prototype.build_portfolioTable = function(portfolioStockList) {
	this.appendChild(portfolioTable_table(portfolioStockList));
}



function portfolioInfo_basechart(renderTarget, dataTarget) {
	var chart = new Highcharts.Chart({
		chart: {
			renderTo: renderTarget
		},
		tooltip: {
            pointFormat: '<b>${point.y:.2f}</b>'
        },
		plotOptions: {
			pie: {
				dataLabels: {
					formatter: function() {
						if(this.y > 0) {
							return this.point.company;
						}
					}
				}
			}
		}
	});
	chart.addSeries({
		type: "pie",
		name: "value",
		data: dataTarget
	});
	return chart;
}

/*
function portfolioInfo_addchart(chart, dataName, dataTarget, dataIndex){
}
*/

function portfolioInfo_setchart(chart, dataName, dataTarget) {
	for (s in chart.series) {
		if (chart.series[s].name == dataName) {
			return chart.series[s].setData(dataTarget);
		}
	}
}




function portfolioHistory_basechart(renderTarget) {
	return new Highcharts.StockChart({
		chart: {
			renderTo: renderTarget
		},
		plotOptions: {
			area: {
				stacking: 'normal',
				trackByArea: true,
				//cursor: 'pointer',
				point: {
					events: {
						click: function(e) {
							portfolioInfo_setchart(infoChart, "value", this.stocks);
						}
					}
				}
			}
		},
		tooltip: {
			headerFormat: '<span style="font-size: 10px">{point.key}</span><br/>',
            pointFormat: '<span style="color:{series.color}">\u25CF</span> {series.name}: <b>{point.x}, ${point.y:.2f}</b><br/>',
			
        },
		rangeSelector: {
			enabled: true
		},
		xAxis: {
			ordinal: false
		}
	});
}



function portfolioHistory_addchart(chart, dataName, dataTarget, dataIndex) {
	return chart.addSeries({
		name: dataName,
		data: dataTarget,
		type: 'area',
		index: dataIndex
	});
}

function getStockValue(stock, unixtime) {
	var values = Object.keys(stockValues[stock]);
	
	var bestValue = 0;
	for (var v in values) {
		if (values[v] >= unixtime) {
			if (values[v] == unixtime) {
				bestValue = values[v];
			}
			break;
		}
		if(values[v] > bestValue) {
			bestValue = values[v];
		}
	}
	return stockValues[stock][bestValue];
}






function populateHistory(portfolioHistory) {
	var chartData = {};
	
	chartData["cash"] = [];
	chartData["comp"] = [];
	chartData["stock"] = [];
	
	/*
	chartData["stock_individual"] = [];
	for(var v in stockValues) {
		chartData["stock_individual"][v] = [];
	}
	*/
	
	for(var h in portfolioHistory) {
		// CHANGE FOR JSON //////////////////////////////////////////////////////////////////////////////
		var date = portfolioHistory[h].unixtime * 1000;
		var valueCash = portfolioHistory[h].cash_value;
		var valueComp = portfolioHistory[h].comp_value;
		var countStocks = portfolioHistory[h].stock_count;
		
		chartData["cash"].push([date, valueCash]);
		chartData["comp"].push([date, valueComp]);
		
		var valueStockSum = 0;
		var valueStocks = [];
		for(var s in stockValues) {
			var count = countStocks[s];
			var value = getStockValue(s, date/1000);
		
			var valueStock = count * value || 0;
			//chartData["stock_individual"][s].push([date, valueStock]);
			valueStockSum += valueStock;
			valueStocks.push({"name":s, "y":valueStock, "count":count, "value":value});
		}
		chartData["stock"].push({"x":date, "y":valueStockSum, "stocks":valueStocks});
	}
	
	
	portfolioHistory_addchart(historyChart, "cash", chartData["cash"], 2);
	portfolioHistory_addchart(historyChart, "comp", chartData["comp"], 1);
	portfolioHistory_addchart(historyChart, "stock", chartData["stock"], 0);
	
	/*
	for (var s in chartData["stock_individual"].reverse()) {
		console.log(historyChart, test, "stock", s, chartData["stock_individual"][s]);
		portfolioHistory_addchart_drilldown(historyChart, test, "stock", s, chartData["stock_individual"][s]);
	}
	*/
}



// TODO: make this apply to actual portfolio stocks
var myPortfolioStocks = [
	{"symbol":"AAPL", "company":"Apple Inc.", "current_value":95.00},
	{"symbol":"GOOG", "company":"Google Inc.", "current_value":100.00},
];


var myPortfolioHistory = [
	{"unixtime":1417805000, "cash_value":9925.00, "comp_value":0.00, "stock_count":{"AAPL":0, "GOOG": 1}},
	{"unixtime":1417805053, "cash_value":9525.00, "comp_value":400.00, "stock_count":{"AAPL":0, "GOOG": 1}},
	{"unixtime":1417891550, "cash_value":9230.00, "comp_value":400.00, "stock_count":{"AAPL":1, "GOOG": 5}},
	{"unixtime":1417891551, "cash_value":9140.00, "comp_value":400.00, "stock_count":{"AAPL":1, "GOOG": 6}},
	{"unixtime":1417891552, "cash_value":9220.00, "comp_value":400.00, "stock_count":{"AAPL":0, "GOOG": 6}},
	{"unixtime":1417891553, "cash_value":9320.00, "comp_value":500.00, "stock_count":{"AAPL":0, "GOOG": 4}},
	{"unixtime":1417891556, "cash_value":9270.00, "comp_value":550.00, "stock_count":{"AAPL":0, "GOOG": 4}},
	{"unixtime":1417977953, "cash_value":9170.00, "comp_value":650.00, "stock_count":{"AAPL":0, "GOOG": 4}},
	{"unixtime":1417977956, "cash_value":9220.00, "comp_value":600.00, "stock_count":{"AAPL":0, "GOOG": 4}},
	{"unixtime":1418064353, "cash_value":9820.00, "comp_value":0.00, "stock_count":{"AAPL":0, "GOOG": 4}},
];


// TODO: make this apply to actual portfolios
var myPortfolio = new Portfolio("Portfolio1", 5000, 7500, 0, null, myPortfolioStocks, myPortfolioHistory);

var stockValues = {
	"AAPL":{
		1417805000: 500
	},
	"GOOG":{
		1417805000: 100,
		1417977953: 500
	},
};


document.getElementById("title").build_portfolioTitle(myPortfolio);
document.getElementById("summary").build_portfolioSummary(myPortfolio);
document.getElementById("detail").build_portfolioTable(myPortfolioStocks);

/*
populateInfo(myPortfolioStocks);
*/
populateHistory(myPortfolioHistory);