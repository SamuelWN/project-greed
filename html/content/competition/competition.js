function Competition(name, unixtimeStart, unixtimeLength, ownerAccountId, entryfee, members) {
	this.name = name;

	this.dateStart = new Date();
	this.dateStart.setTime(unixtimeStart * 1000);

	this.dateEnd = new Date();
	this.dateEnd.setTime((unixtimeStart + unixtimeLength) * 1000);

	this.ownerAccountId = ownerAccountId;
	this.entryfee = entryfee;

	this.members = members;
}

function competitionTable_tr_th() {
	var tr = document.createElement("tr");

	var th_member = document.createElement("th");
	th_member.appendChild(document.createTextNode("Member"));

	var th_valueTotal = document.createElement("th");
	th_valueTotal.appendChild(document.createTextNode("Total Value"));

	tr.appendChild(th_member);
	tr.appendChild(th_valueTotal);

	return tr;
}

function competitionTable_tr_td(member) {
	var tr = document.createElement("tr");

	var td_member = document.createElement("td");
	td_member.appendChild(document.createTextNode(member.account + " - " + member.portfolio)); //////////////////////////////////////////

	var td_valueTotal = document.createElement("td");
	td_valueTotal.className = "dollars";
	td_valueTotal.appendChild(document.createTextNode(member.valueTotal)); //////////////////////////////////////////

	tr.appendChild(td_member);
	tr.appendChild(td_valueTotal);

	return tr;
}

function competitionTable_table(competitionMembers) {
	var table = document.createElement("table");
	table.appendChild(competitionTable_tr_th());
	for (var member in competitionMembers) {
		table.appendChild(competitionTable_tr_td(competitionMembers[member]));
	}
	return table;
}

function competitionTitle_span(competition) {
	return document.createTextNode(competition.name);
}

function competitionSummary_dl(competition) {
	var dl = document.createElement("dl");

	var dt_dateStart = document.createElement("dt");
	dt_dateStart.appendChild(document.createTextNode("Start Date"));
	var dd_dateStart = document.createElement("dd");
	dd_dateStart.appendChild(document.createTextNode(competition.dateStart.toString()));

	var dt_dateEnd = document.createElement("dt");
	dt_dateEnd.appendChild(document.createTextNode("End Date"));
	var dd_dateEnd = document.createElement("dd");
	dd_dateEnd.appendChild(document.createTextNode(competition.dateEnd.toString()));

	var dt_entryFee = document.createElement("dt");
	dt_entryFee.appendChild(document.createTextNode("Entry Fee"));
	var dd_entryFee = document.createElement("dd");
	dd_entryFee.className = "dollars";
	dd_entryFee.appendChild(document.createTextNode(competition.entryfee));

	var dt_owner = document.createElement("dt");
	dt_owner.appendChild(document.createTextNode("Creator"));
	var dd_owner = document.createElement("dd");
	dd_owner.appendChild(document.createTextNode(competition.ownerAccountId));

	dl.appendChild(dt_dateStart);
	dl.appendChild(dd_dateStart);
	dl.appendChild(dt_dateEnd);
	dl.appendChild(dd_dateEnd);
	dl.appendChild(dt_entryFee);
	dl.appendChild(dd_entryFee);
	dl.appendChild(dt_owner);
	dl.appendChild(dd_owner);

	return dl;
}

Element.prototype.build_competitionTitle = function (competition) {
	this.appendChild(competitionTitle_span(competition));
}

Element.prototype.build_competitionSummary = function (competition) {
	this.appendChild(competitionSummary_dl(competition));
}

Element.prototype.build_competitionTable = function (competition) {
	this.appendChild(competitionTable_table(competition.members));
}

// TODO: make this apply to actual competition members
var competitionMembers = [{
		"account" : "a1",
		"portfolio" : "p1",
		"valueTotal" : 123.45
	}, {
		"account" : "a2",
		"portfolio" : "p2",
		"valueTotal" : 234.56
	}, {
		"account" : "a3",
		"portfolio" : "p3",
		"valueTotal" : 345.67
	},
];

// TODO: make this apply to actual competitions
var myCompetition = new Competition("comp2", 1417891553, 86400, 1, 500.0, competitionMembers);

document.getElementById("title").build_competitionTitle(myCompetition);
document.getElementById("summary").build_competitionSummary(myCompetition);
document.getElementById("detail").build_competitionTable(myCompetition);
