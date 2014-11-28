function TopPortfolio(id, name, accountid, username, value) {
	this.id = id;
	this.name = name;
	this.accountid = accountid;
	this.username = username;
	this.value = value;
}

// TODO: make this apply to actual top portfolios
var topPortfolios = [
	//new TopPortfolio(9, "TheWinner", 3, "gdimitoglou", 99999),
	new TopPortfolio(5, "Portfolio3", 1, "myura", 50000),
	//new TopPortfolio(6, "AnotherPort", 2, "pwallice", 43298),
	new TopPortfolio(2, "Portfolio2", 1, "myura", 20020),
	new TopPortfolio(1, "Portfolio1", 1, "myura", 10001)
];


/*
<li>
	<dl>
		<dt>{username}</dt>
		<dd class="leaderboard_portfolio">{portfolio name}</dd>
		<dd class="leaderboard_value dollars">{portfolio value}</dd>
	</dl>
</li>
*/

function leaderboard_li(topPortfolio) {
	var li = document.createElement("li");
	
	var dl = document.createElement("dl");
	
	var dt = document.createElement("dt");
	dt.appendChild(document.createTextNode(topPortfolio.username));
	
	var dd_portfolio = document.createElement("dd");
	dd_portfolio.className = "leaderboard_portfolio";
	dd_portfolio.appendChild(document.createTextNode(topPortfolio.name));
	
	var dd_value = document.createElement("dd");
	dd_value.className = "leaderboard_value dollars";
	dd_value.appendChild(document.createTextNode(topPortfolio.value));
	
	dl.appendChild(dt);
	dl.appendChild(dd_portfolio);
	dl.appendChild(dd_value);
	
	li.appendChild(dl);
	return li;
}

Element.prototype.build_leaderboard = function(topPortfolioList) {
	var ol = this.lastElementChild;
	var count = 0;
	for (var topPortfolio in topPortfolioList) {
		ol.appendChild(leaderboard_li(topPortfolioList[topPortfolio]));
		count++;
	}
	for (count; count < 5; count++) {
		ol.appendChild(leaderboard_li(new TopPortfolio(undefined, "-----", undefined, "-----", 0)));
	}
}

document.getElementById("leaderboard").build_leaderboard(topPortfolios);