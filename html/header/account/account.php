<?php

/*
$stockString = $_GET['s'];
$stockScript = '../engines/search.py';
$stockCommand = $stockScript . ' ' . $stockString;

$command = escapeshellcmd($stockCommand);
$output = shell_exec($command);
echo $output;
*/

$json = '{"id":1,"username":"myura"}';
$account = json_decode($json, true);

$myAccount = "var myAccount = new Account(" . $account["id"] . ", '" . $account["username"] . "');"
	."\n"."document.getElementById('account_first').modify_account_first(myAccount);"
	."\n"."document.getElementById('account_last').modify_account_last(myAccount);"
	;

echo $myAccount

?>