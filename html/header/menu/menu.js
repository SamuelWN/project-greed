function Portfolio(id, name, value) {
	this.id = id;
	this.name = name;
	this.value = value;
}

// TODO: make this apply to actual portfolios and their values
var myPortfolios = [
	new Portfolio(1, "Portfolio1", 10001),
	new Portfolio(2, "Portfolio2", 20020),
	new Portfolio(5, "Portfolio3", 50000)
];
var currentPortfolio = 0;


function menu_portfolio_a(portfolio) {
	var a = document.createElement("a");
	var textNode;
	if (portfolio === undefined) {
		textNode = document.createTextNode("+ new portfolio");
	} else {
		textNode = document.createTextNode(portfolio.name + " [" + portfolio.value + "]");
	}
	a.appendChild(textNode);
	a.setAttribute("href", "#")
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








Element.prototype.build_whatif = function() {
	var a = document.createElement("a");
	var textNode = document.createTextNode("What If..?");
	a.appendChild(textNode);
	a.setAttribute("href", "#");
	this.appendChild(a);
}









document.getElementById("menu_portfolio").build_portfolio(currentPortfolio, myPortfolios);
document.getElementById("menu_whatif").build_whatif(currentPortfolio, myPortfolios);