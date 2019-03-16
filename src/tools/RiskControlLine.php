<?php

$lower = 95;    // 单月最大亏损
$higher = 105;  // 单月最大盈利

$times = 1000;  // 测试轮回数（年数）
$sum = 0.0;

for ($i=0; $i < $times; $i++) { 

	$init = 1.0;  // 初始值
	$num = 12;  // 12个月

	for($j = 1; $j <= $num; $j++){
  		$r = round(mt_rand($lower,$higher)/100.0,5);
  		$init = round($init * $r,3);
	}

	$sum += $init;
}

$r = ($sum/$times - 1.0)*100.0;
echo "\n平均收益率：$r%\n";





