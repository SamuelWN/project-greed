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


// global chart options
Highcharts.setOptions({
	chart: {
		backgroundColor: "transparent",
		style: {
            fontFamily: 'serif'
        }
	},
	credits: {
		enabled: false
	},
	title: {
		text: null
	}
});


include("header/header.js");
include("sidebar/sidebar.js");
include("content/content.js");
include("footer/footer.js");