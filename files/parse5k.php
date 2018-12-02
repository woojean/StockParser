<?php

/*
http://pdfm2.eastmoney.com/EM_UBG_PDTI_Fast/api/js?id=0000011&TYPE=m5k&js=fsData1543740954489_46245425((x))&rtntype=5&isCR=false&authorityType=fa&fsData1543740954489_46245425=fsData1543740954489_46245425
*/

$path = '/Users/wujian/woojean/StockParser/files/000001-5分钟K线.json';
$report = '/Users/wujian/woojean/StockParser/files/000001-5分钟K线.html';

$s = file_get_contents($path);

$data = json_decode($s,true);

// 解析
$parsedData = [];
foreach ($data as $v) {

	$items = explode(',', $v);

	$date = substr($items[0], 0,10);
	if(!isset($parsedData[$date])){
		$parsedData[$date] = [];
	}
	$time = substr($items[0], 11,5);
    $minPrice = floatval($items[4]);
    $maxPrice = floatval($items[3]);
	$parsedData[$date][] = [$time,$minPrice,$maxPrice];
}

// 排序
$sortedData = [];
foreach ($parsedData as $date => $v) {
	$minPrice = 9999999;
	$maxPrice = 0;
	$minPriceItem = [];
	$maxPriceItem = [];
	foreach ($v as $item) {
		if($item[1] < $minPrice){
			$minPriceItem = $item;
			$minPrice = $item[1];
		}
		if($item[2] > $maxPrice){
			$maxPriceItem = $item;
			$maxPrice = $item[2];
		}
	}
	$sortedData[$date] = [$minPriceItem,$maxPriceItem];
}


// 渲染
$html = '<table>';
foreach ($sortedData as $date => $data) {
	$html .='<tr>';
	$html .= '<td>'.$date.'</td>';
	$html .= '<td>'.$data[0][0].'</td>';
	$html .= '<td>'.$data[0][1].'</td>';
	$html .= '<td>'.$data[1][0].'</td>';
	$html .= '<td>'.$data[1][2].'</td>';
	$html .='</tr>';
}
$html .= '</table>';

// $html = json_encode($sortedData);
file_put_contents($report,$html);
system('open ' . $report);
