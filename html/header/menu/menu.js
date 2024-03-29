function Portfolio(id, name, value) {
	this.id = id;
	this.name = name;
	this.value = value;
}

function menu_portfolio_a(portfolio) {
	var a = document.createElement("a");

	if (portfolio === undefined) {
		a.appendChild(document.createTextNode("+ new portfolio"));
		a.href = "." + "?" + "pn=" + 1;
	} else {
		var span = document.createElement("span");
		span.appendChild(document.createTextNode(portfolio.value));
		span.className = "dollars";

		a.appendChild(document.createTextNode(portfolio.name + " ["));
		a.appendChild(span);
		a.appendChild(document.createTextNode("]"));

		a.href = "." + "?" + "p=" + portfolio.id;
	}
	return a;
}

function menu_portfolio_li(portfolio) {
	var li = document.createElement("li");
	li.appendChild(menu_portfolio_a(portfolio));
	return li;
}

Element.prototype.build_portfolio = function (portfolioCurrent, portfolioList) {
	this.appendChild(menu_portfolio_a(portfolioList[portfolioCurrent]));

	var ul = document.createElement("ul");
	for (var portfolio in portfolioList) {
		ul.appendChild(menu_portfolio_li(portfolioList[portfolio]));
	}
	ul.appendChild(menu_portfolio_li());
	this.appendChild(ul);
}

/*
// TODO: make this apply to actual portfolios and their values
var myPortfolios = [
	new Portfolio(1, "Portfolio1", 10001),
	new Portfolio(2, "Portfolio2", 20020),
	new Portfolio(5, "Portfolio3", 50000)
];
var currentPortfolio = 0;

document.getElementById("menu_portfolio").build_portfolio(currentPortfolio, myPortfolios);
*/
