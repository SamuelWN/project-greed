var params = getUrlParams();

if ("p" in params) {
	include("content/portfolio/portfolio.js");
} else if ("s" in params) {
	include("content/stock/stock.js");
} else if ("sf" in params) {
	include("content/search/search.js");
} else if ("c" in params) {
	include("content/competition/competition.js");
}
