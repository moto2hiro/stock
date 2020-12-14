$web = New-Object System.Net.WebClient
$str = $web.DownloadString("http://127.0.0.1:5000/api/stock/delete_old_prices")