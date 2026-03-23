<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="csrf-token" content="{{ csrf_token() }}">
    <link rel="stylesheet" href="https://unpkg.com/snes.css@1.0.1/dist/snes.min.css">
    @vite('resources/css/style.css')
    <title>Space Vault</title>
    <link rel="icon" type="image/x-icon" href="{{ asset('favicon.ico') }}">
    <style>
        body {
            background-image: url("{{ asset('images/background.png')}}");
            background-repeat: no-repeat;
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }
    </style>
</head>

<body>
    <div class="dashboard">
        <div class="title">
            <h1>SPACE VAULT v1.0</h1>
            <h2>Welcome {{ $user->username }}!</h1>
            <h3>Current balance: ${{ round($user->balance) }}</h2>
            @if (Route::currentRouteName() !== 'dashboard')
                <a href="/" class="back-dashboard">Dashboard</a>
            @endif
        </div>
        
        @yield('content')

        <div class="logout">
            <form method="POST" action="/logout">
                @csrf
                @method("DELETE")
                <input type="submit" value="Log Out">
            </form>
        </div>
    </div>
</body>
</html>
