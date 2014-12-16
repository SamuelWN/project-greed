<?php
$engineDir = '../../engines';
$stockScript = 'search.py';
$stockParams = $_GET['q'];
$stockCommand = $engineDir . '/' . $stockScript . ' ' . $stockParams;

$command = escapeshellcmd($stockCommand);
$json = shell_exec($command);

echo $json;
?>
