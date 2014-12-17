<?php
session_start();

if (isset($_SESSION["account_id"])) {
	$account_id = $_SESSION["account_id"];
	
	$engineDir = '../../engines';
	$stockScript = 'account_engine.py';
	$stockParams = '-iI ' . $account_id;
	$stockCommand = $engineDir . '/' . $stockScript . ' ' . $stockParams;

	$command = escapeshellcmd($stockCommand);
	$json = shell_exec($command);

	$account = json_decode($json, true);
	
	$myAccount = "myAccount" . "_" . substr(str_shuffle("abcdefghijklmnopqrstuvwxyz"), 0, 8);
	$javascript = "var " . $myAccount . " = new Account(" . $account["id"] . ", '" . $account["username"] . "');"
		."\n"."document.getElementById('account_first').modify_account_first(" . $myAccount . ");"
		."\n"."document.getElementById('account_last').modify_account_last(" . $myAccount . ");"
		;
	echo $javascript;
	
	
	$myPortfolios = "var myPortfolios = ["
	."\n"."new Portfolio(1, 'Portfolio1', 10001),"
	."\n"."new Portfolio(2, 'Portfolio2', 20020),"
	."\n"."new Portfolio(5, 'Portfolio3', 50000)"
	."\n"."];"
	."\n"."var currentPortfolio = 0;"
	."\n"."document.getElementById('menu_portfolio').build_portfolio(currentPortfolio, myPortfolios);"
	;
	
	echo $myPortfolios;
}
?>