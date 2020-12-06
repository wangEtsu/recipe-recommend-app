@extends('layouts.app')

@section('content')
    <h1>Recipes</h1>
    @if(count($recipes) > 1)
        @foreach($recipes as $recipe)
            <div class="well">
                <h3>{{ $recipe->recipe_name }}</h3>
            <div>
        @endforeach
    @else
        <p>No Recipes Found</p>
    @endif
@endsection

