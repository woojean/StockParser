<?php

$lower = 95;    // 单月最大亏损
$higher = 110;  // 单月最大盈利

$times = 1000;  // 测试轮回数（年数）
$sum = 0.0;

for ($i=0; $i < $times; $i++) { 

	$init = 1.0;  // 初始值
	$num = 12;  // 12个月

	for($j = 1; $j <= $num; $j++){
		$d = (mt_rand($lower,$higher) - 100)/100.0;
		// echo "\n获利：".strval($d*100.0).'%';
  		$init += $d;
	}

	$sum += $init;
	echo "\n获利：".strval(($init-1.0)*100.0).'%';
}

$r = ($sum/$times - 1.0)*100.0;
echo "\n平均收益率：$r%\n";
