function Account(id, username) {
	this.id = id;
	this.username = username;
}

Element.prototype.modify_account_first = function (account) {
	var a_first = this.firstElementChild;
	a_first.innerHTML = account.username;
	a_first.href = "#";
}

Element.prototype.modify_account_last = function () {
	var a = this.firstElementChild;
	a.innerHTML = "logout";
	a.href = "javascript:clearSession();";
}
