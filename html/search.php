<?php

$engineDir = '../engines';

$stockString = $_GET['q'];
$stockScript = 'search.py';
$stockCommand = $engineDir . '/' . $stockScript . ' ' . $stockString;

$command = escapeshellcmd($stockCommand);
$output = shell_exec($command);
echo $output;
?>
