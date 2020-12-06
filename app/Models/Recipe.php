<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class Recipe extends Model
{
    use HasFactory;

    // Table Name
    protected $table = 'recipe';
    //Primary Key
    public $primaryKey = 'recipe_id';
}
