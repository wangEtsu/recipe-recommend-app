## About Sugar Detective
*Insert Description Here*

## How To Run Sugar Detective
1. set up project folder and pull the repo

```cd anywhere```

```mkdir sugar-detective```

```git clone https://github.com/wangEtsu/sugar-detective.git```

2. Download XAMPP & Composer (Or WAMP/LAMP based on your OS)

You can get XAMPP here: https://www.apachefriends.org/index.html

And Compser here: https://getcomposer.org/

*You might want to set up XAMPP first if you don't have PHP installed*

3. Install dependencies

Inside the project folder, run:

```composer install```

4. Start the server

```php artisan serve```

## Troubleshooting

Incase you meet such error:

```PHP Fatal error:  Unknown: Failed opening required 'D:\XAMPP\htdocs\sugar-detective\server.php'```

Please check if server.php is there, there are chances that it will be removed by anti-virus software