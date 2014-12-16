<?php
$engineDir = '../../engines';
$stockScript = 'find_by_symbol.py';
$stockParams = $_GET['s'];
$stockCommand = $engineDir . '/' . $stockScript . ' ' . $stockParams;

$command = escapeshellcmd($stockCommand);
$json = shell_exec($command);

echo $json;
?>
