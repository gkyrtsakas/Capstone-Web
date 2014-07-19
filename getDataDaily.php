<?php

$con=mysqli_connect("127.0.0.1", "root", "root", "mysql");
if (mysqli_connect_errno())
{
	echo "Failed to connect to database: ".mysqli_connect_errno();
}

$result = mysqli_query($con, "SELECT
  MONTH(`date`) as za_month,
  DAY(`date`) as za_day,
  SUM(current*voltage) as total
FROM
  data1
WHERE MONTH(`date`) = MONTH(NOW())
GROUP BY
  za_month,
  za_day
ORDER BY
  date ASC;");
if (!$result) { // add this check.
    die('Invalid query: ' . mysql_error());
}

$table = array();
$table['cols'] = array (
array('id' => '', 'label' => 'Date', 'pattern' => "", 'type' => 'string'),
array('id' => '', 'label' => 'System Energy (Wh)', 'pattern' => "", 'type' => 'number')
);

$rows = array();

while ($row = $result->fetch_assoc())
{
	$temp = array();
	$temp[] = array('v' => (string)$row['za_day'], 'f' => NULL);
	$temp[] = array('v' => (double)$row['total'], 'f' => NULL);
	$rows[] = array('c' => $temp);
}
$table['rows'] = $rows;

$output = json_encode($table);

mysqli_close($con);

echo $output;


?>