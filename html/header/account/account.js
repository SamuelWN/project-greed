function Account(id, username) {
	this.id = id;
	this.username = username;
}

Element.prototype.modify_account_first = function (account) {
	var a_first = this.firstElementChild;
	a_first.innerHTML = account.username;
	a_first.setAttribute("href", "#");
}

Element.prototype.modify_account_last = function () {
	var a = this.firstElementChild;
	a.innerHTML = "logout";
	a.setAttribute("href", "#");
}

// TODO: make this apply to actual accounts
var myAccount = new Account(1, "myura");

document.getElementById("account_first").modify_account_first(myAccount);
document.getElementById("account_last").modify_account_last(myAccount);
