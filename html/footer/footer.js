function footer_span() {
	var span = document.createElement("span");
	span.appendChild(document.createTextNode("CS 324, ©" + new Date().getFullYear()));
	return span;
}

Element.prototype.build_footer = function() {
	this.appendChild(footer_span());
}

document.getElementById("footer").build_footer();