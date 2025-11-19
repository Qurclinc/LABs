<?php

// Дана строка. Если ее длина больше 10, то оставить в строке только первые 6 символов, 
// иначе дополнить строку символами 'o' до длины 12.

$string = "Aboba";
$new_string = "";
if (strlen($string) > 10) {
    for ($i = 0; $i < 6; $i++) {      
        $new_string = "$new_string$string[$i]";
    }
} else {
    $new_string = $string;
    for ($i=0; $i < 12 - strlen($string); $i++) {
        $new_string = "{$new_string}o";
    }
}

echo "$new_string\n";

?>