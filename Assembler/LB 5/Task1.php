<?php

// Найти минимальный элемент массива.

$arr = [14, 20, 30, 10, 5, 78, 52, 11, 30];
$min = $arr[0];
for ($i=0; $i < sizeof($arr) ; $i++) { 
    $elem = $arr[$i];
    if ($elem <= $min) {
        $min = $elem;
    }
    $str = strval($elem);
    echo "$str ";
}
echo "\nMin element is {$min}\n";

?>