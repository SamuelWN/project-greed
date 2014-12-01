function Portfolio(name, valueTotal, valueCash, valueStock, valueComp) {
	this.name = name;
	this.valueTotal = valueTotal;
	this.valueCash = valueCash;
	this.valueStock = valueStock;
	this.valueComp = valueComp;
}

function PortfolioStock(company, symbol, valueTotal, value, count) {
	this.company = company;
	this.symbol = symbol;
	this.valueTotal = valueTotal;
	this.value = value;
	this.count = count;
}



// TODO: make this apply to actual portfolios
var myPortfolio = new Portfolio("Portfolio1", 15000, 5000, 7500, 2500);

// TODO: make this apply to actual portfolio stocks
var portfolioStocks = [
	new PortfolioStock("Apple Inc.", "AAPL", 1847.52, 115.47, 16),
	new PortfolioStock("Google Inc.", "GOOG", 3210.18, 535.03, 6)
];




















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
	span.className = "title";
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

document.getElementById("portfolio_title").build_portfolioTitle(myPortfolio);
document.getElementById("portfolio_summary").build_portfolioSummary(myPortfolio);
document.getElementById("portfolio_table").build_portfolioTable(portfolioStocks);