<?php

$s = file_get_contents('/Users/wujian/woojean/StockParser/data/price/000001');

$s = substr($s, 13);
$s = substr($s, 0,strlen($s)-1);

echo $s;

$data = json_decode($s,True);

$csv = '';
foreach ($data['data'] as $key => $value) {
	$arr = explode(',', $value);
	$csv .= $arr[0].','.$arr[7];
	$csv .= "\n";
}


file_put_contents('/Users/wujian/woojean/StockParser/src/tools/rate.csv', $csv);