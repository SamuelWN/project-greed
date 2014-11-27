<?php
	$user = $_GET["u"];
	$competition = $_GET["c"];
	$stock = $_GET["s"];
	$portfolio = $_GET["p"];
	
	
	$logo_html = file_get_contents('logo.html');
	$top5_html = file_get_contents('top5.html');

	$account_html = file_get_contents('account_out.html');
	
	if(!empty($user)) {
		$account_html = str_replace("{user}", $user, file_get_contents('account_in.html'));
	}
	
	$portfolio_html = "";
	if(!empty($portfolio)) {
		$portfolio_html = str_replace("{portfolio}", $portfolio, file_get_contents('portfolio.html'));
	}
	
	$menu_html = file_get_contents('menu.html');
	if (!empty($portfolio)) {
		$menu_html = str_replace("{portfolio}", $portfolio, file_get_contents('menu.html'));
	}
	
	
	echo "<!DOCTYPE html>";
	echo "<html>";
	
	echo "<head>";
	echo "<link rel=\"stylesheet\" type=\"text/css\" href=\"index.css\">";
	echo "</head>";
	
	echo "<body>";
	
	echo "<div id=\"header\">";
		echo $logo_html;
		echo $account_html;
		echo $menu_html;
	echo "</div>";
	
	echo "<div id=\"sidebar\">";
		echo $top5_html;
	echo "</div>";
	
	echo "<div id=\"content\">";
		echo $portfolio_html;
	echo "</div>";
	
	
	
	echo "</body>";
	echo "</html>";
?>