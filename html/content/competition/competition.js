var chartOptions = {
	animation: false,
	
	segmentShowStroke : true,
	segmentStrokeColor : "black",
	segmentStrokeWidth : 2,
	
	showTooltips: true,
	tooltipTemplate: "<%if (label){%><%=label%>: $<%}%><%= value %>",
};

function Portfolio(name, valueCash, valueStock, valueComp, compEntryFee) {
	this.name = name;
	this.valueCash = valueCash;
	this.valueStock = valueStock;
	this.valueComp = valueComp;
	this.compEntryFee = typeof compEntryFee !== 'undefined' ? compEntryFee : undefined;
	
	this.valueTotal = this.valueCash + this.valueStock + this.valueComp;
}

function PortfolioStock(company, symbol, valueTotal, value, count) {
	this.company = company;
	this.symbol = symbol;
	this.valueTotal = valueTotal;
	this.value = value;
	this.count = count;
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


function portfolioSummary_highcharts(dataTarget, renderTarget) {
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
					/*
					formatter: function() {
						if(this.y > 0) {
							return this.y;
						}
					}
					*/
				}
			}
		}
	});
	
	//chart.showLoading();
	
	chart.addSeries({
		type: "pie",
		name: "value",
		data: [
			["Cash", dataTarget.valueCash],
			["Stock", dataTarget.valueStock],
			["Competition", dataTarget.valueComp]
		]
	});
	
	//chart.hideLoading();
	
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
	
	//dl.appendChild(portfolioSummary_chartjs(portfolio));
	
	var portfolio_chart = document.createElement("div");
	portfolioSummary_highcharts(portfolio, portfolio_chart);
	dl.appendChild(portfolio_chart);
	
	return dl;
}




Element.prototype.build_portfolioTitle = function(portfolio) {
	this.appendChild(portfolioTitle_span(portfolio));
	
}

Element.prototype.build_portfolioSummary = function(portfolio) {
	this.appendChild(portfolioSummary_dl(portfolio));
}

Element.prototype.build_portfolioTable = function(portfolioStockList) {
	this.appendChild(portfolioTable_table(portfolioStockList));
}



// TODO: make this apply to actual portfolios
var myPortfolio = new Portfolio("Portfolio1", 5000, 7500, 0);

// TODO: make this apply to actual portfolio stocks
var portfolioStocks = [
	new PortfolioStock("Apple Inc.", "AAPL", 1847.52, 115.47, 16),
	new PortfolioStock("Google Inc.", "GOOG", 3210.18, 535.03, 6)
];


document.getElementById("title").build_portfolioTitle(myPortfolio);
document.getElementById("summary").build_portfolioSummary(myPortfolio);
document.getElementById("detail").build_portfolioTable(portfolioStocks);