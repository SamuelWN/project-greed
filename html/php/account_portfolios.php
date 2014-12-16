<?php
$engineDir = '../../engines';
$stockScript = 'portfolio_engine.py';
$stockParams = $_GET['a'];
$stockCommand = $engineDir . '/' . $stockScript . ' ' . $stockParams;

$command = escapeshellcmd($stockCommand);
$json = shell_exec($command);

echo $json;
?>
