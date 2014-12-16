var included = new Array;
function include(filename) {
	if (!(included.indexOf(filename) > -1)) {
		included.push(filename);
		//var head = document.getElementsByTagName('head')[0];
		var js = document.getElementById('js');
		script = document.createElement('script');
		script.src = filename;
		script.type = 'text/javascript';
		// head.appendChild(script);
		js.appendChild(script);
	}
}

function getUrlParams() {
	params = {};

	var queryString = window.location.search.substring(1);
	var vars = queryString.split('&');
	for (var v in vars) {
		var varComponents = vars[v].split('=');
		var key = varComponents[0];
		var val = varComponents[1];
		if (val.trim()) {
			params[decodeURIComponent(key)] = decodeURIComponent(val);
		}
	}
	return params;
}

function setSession(account_id, portfolio_id, toDelete) {
	var sessionPhp = "/greed/php/session.php";
	var commands = [];
	if (account_id != null) {
		commands.push("a=" + account_id);
	}
	if (portfolio_id != null) {
		commands.push("p=" + account_id);
	}
	if (toDelete == true) {
		commands.push("d=" + 1);
	}
	var httpRequest = new XMLHttpRequest;
	httpRequest.onreadystatechange = function () {
		if (httpRequest.readyState == 4) {
			if (httpRequest.status == 200) {
				var responseObject = JSON.parse(this.responseText);
				document.getElementById("detail").build_searchTable(responseObject);
			}
		}
	}
	httpRequest.open('GET', sessionPhp + "?" + commands.join("&"), false);
	httpRequest.send();

	document.location.reload();
}

function clearSession() {
	setSession(null, null, true);
}

function login() {
	setSession(1, null);
}

// global chart options
Highcharts.setOptions({
	global : {
		timezoneOffset : new Date().getTimezoneOffset(),
	},
	chart : {
		backgroundColor : "transparent",
		style : {
			fontFamily : 'serif'
		}
	},
	credits : {
		enabled : false
	},
	title : {
		text : null
	}
});

include("header/header.js");
include("sidebar/sidebar.js");
include("content/content.js");
include("footer/footer.js");
