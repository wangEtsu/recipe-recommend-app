<?php

use Illuminate\Support\Facades\Route;

/*
|--------------------------------------------------------------------------
| Web Routes
|--------------------------------------------------------------------------
|
| Here is where you can register web routes for your application. These
| routes are loaded by the RouteServiceProvider within a group which
| contains the "web" middleware group. Now create something great!
|
*/

// Laravel 8 change the routing to this format
Route::get('/', 'App\Http\Controllers\PagesController@index');

Route::get('/about', function () {
    return view('pages.about');
});

// Route::get('/user/{id}/{name}', function ($id, $name) {
//     return 'This is user ' . $name . ' with an id of ' . $id;
// });

Auth::routes();

Route::get('/home', [App\Http\Controllers\HomeController::class, 'index'])->name('home');
