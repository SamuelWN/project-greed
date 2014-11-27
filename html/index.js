var included = new Array;
function include(filename) {
	if (!(included.indexOf(filename) > -1)) {
		included.push(filename);
		var head = document.getElementsByTagName('head')[0];
		script = document.createElement('script');
		script.src = filename;
		script.type = 'text/javascript';
		head.appendChild(script);
	}
}

function include_jquery() {
	include("jquery.min.js");
}

include("header.js");