function footer_span() {
	return document.createTextNode("©" + new Date().getFullYear());
}

Element.prototype.build_footer = function () {
	this.appendChild(footer_span());
}

document.getElementById("footer").build_footer();
