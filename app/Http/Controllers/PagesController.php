<?php

namespace App\Http\Controllers;

// so it can handle request
use Illuminate\Http\Request;

class PagesController extends Controller
{
    public function index(){
        $title = "Pass something";
        return view('pages.index', compact('title'));
    }

    public function about(){
        return view('pages.about');
    }
}
