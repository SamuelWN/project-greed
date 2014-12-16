<?php
session_start();

if (array_key_exists('d', $_GET)) {
	session_unset();
	session_destroy();
	return;
}

if (array_key_exists('a', $_GET)) {
	$_SESSION["account_id"] = $_GET['a'];
}

if (array_key_exists('p', $_GET)) {
	$_SESSION["portfolio_id"] = $_GET['p'];
}

if (array_key_exists('w', $_GET)) {
	//if (isset($_SESSION["account_id"])) {
		echo "account_id: " . $_SESSION["account_id"];
	//}
	echo "<br/>";
	//if (isset($_SESSION["portfolio_id"])) {
		echo "portfolio_id: " . $_SESSION["portfolio_id"];
	//}
}
?>
