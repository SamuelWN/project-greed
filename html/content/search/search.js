function searchTitle_span() {
	return document.createTextNode("Find");
}

function searchSummary_form() {
	var form = document.createElement('form');

	var searchbar = document.createElement("input");
	searchbar.type = "search";
	searchbar.name = "q";

	var submit = document.createElement("input");
	submit.type = "submit"
		submit.name = "Search";

	form.preventDefault = true;
	form.onsubmit = function () {
		callSearch(this.q.value);
		return false;
	};

	form.appendChild(searchbar);
	form.appendChild(submit);
	return form;
}

function searchTable_tr_th() {
	var tr = document.createElement("tr");

	var th_company = document.createElement("th");
	th_company.className = "company";
	th_company.appendChild(document.createTextNode("Company"));

	var th_symbol = document.createElement("th");
	th_symbol.appendChild(document.createTextNode("Stock"));

	var th_value = document.createElement("th");
	th_value.appendChild(document.createTextNode("Value"));

	tr.appendChild(th_company);
	tr.appendChild(th_symbol);
	tr.appendChild(th_value);

	return tr;
}

function searchTable_td_buy() {
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

	td.appendChild(input_number);
	td.appendChild(input_buy);

	return td;
}

function searchTable_tr_td(stock) {
	var symbol = stock.symbol;
	var company = stock.company;
	var value = stock.value;

	var tr = document.createElement("tr");

	var td_company = document.createElement("td");
	td_company.className = "company";
	td_company.appendChild(document.createTextNode(company));

	var td_symbol = document.createElement("td");

	var td_symbol_a = document.createElement("a");
	td_symbol_a.href = "." + "?s=" + symbol;
	td_symbol_a.appendChild(document.createTextNode(symbol));

	td_symbol.appendChild(td_symbol_a);

	var td_value = document.createElement("td");
	td_value.className = "dollars";
	td_value.appendChild(document.createTextNode(value));

	tr.appendChild(td_company);
	tr.appendChild(td_symbol);
	tr.appendChild(td_value);
	tr.appendChild(searchTable_td_buy());

	return tr;
}

function searchTable_table(searchResults) {
	var table = document.createElement("table");
	table.appendChild(searchTable_tr_th());

	for (var s in searchResults) {
		var stock = searchResults[s];
		table.appendChild(searchTable_tr_td(stock));
	}

	return table;
}

Element.prototype.build_searchTitle = function () {
	this.appendChild(searchTitle_span());
}

Element.prototype.build_searchSummary = function () {
	this.appendChild(searchSummary_form());
}

Element.prototype.build_searchTable = function (searchResults) {
	this.replaceChild(searchTable_table(searchResults), this.childNodes[0]);
}

var callSearchPhp = "/greed/php/search.php";
function callSearch(query) {
	var httpRequest = new XMLHttpRequest;
	httpRequest.onreadystatechange = function () {
		if (httpRequest.readyState == 4) {
			if (httpRequest.status == 200) {
				var responseObject = JSON.parse(this.responseText);
				document.getElementById("detail").build_searchTable(responseObject);
			}
		}
	}
	httpRequest.open('GET', callSearchPhp + "?" + "q=" + query, true);
	httpRequest.send();
}

document.getElementById("title").build_searchTitle();
document.getElementById("summary").build_searchSummary(); ;
