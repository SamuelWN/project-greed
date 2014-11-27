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
	return a;
}

function menu_portfolio_ul(portfolioList) {
	var ul = document.createElement("ul");
	for (var portfolio in portfolioList) {
		ul.appendChild(menu_portfolio_li(portfolioList[portfolio]));
	}
	ul.appendChild(menu_portfolio_li());
	return ul;
}


function build_menu_portfolio(li, portfolioCurrent, portfolioList) {
	li.appendChild(menu_portfolio_list(portfolioList));
}


















var menu_portfolio = document.getElementById("menu_portfolio");
menu_portfolio.appendChild(menu_portfolio_a(myPortfolios[currentPortfolio]));
menu_portfolio.appendChild(menu_portfolio_ul(myPortfolios));



