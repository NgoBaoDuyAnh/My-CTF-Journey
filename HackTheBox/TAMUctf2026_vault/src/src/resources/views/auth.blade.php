@extends('layouts.unauthenticated')

@section('content')
    <div class="title">
        <h1>Intergalactic Space Vault</h1>
    </div>

    @if ($type === "login")
        <div class="content-box">
            <h2>Login</h2>
            <form method="post">
                @csrf
                <label for="username">Username</label>
                <input id="username" name="username"/>
                <label for="password">Password</label>
                <input id="password" name="password" type="password"/>
                <input class="submit" type="submit">
            </form>

            <div class="no-account">
                Don't have an account? Register <a href="{{ route('register') }}">here</a>.
            </div>

            @if ($errors->any())
                <div class="errors">
                    @foreach ($errors->all() as $error)
                        <li>{{ $error }}</li>
                    @endforeach
                </div>
            @endif
        </div>
    @else
        <div class="content-box">
            <h2>Register</h2>
            <form method="post">
                @csrf
                <label for="username">Username</label>
                <input id="username" name="username" />
                <label for="password">Password</label>
                <input id="password" name="password" type="password"/>
                <label for="password2">Confirm Password</label>
                <input id="password2" name="password2" type="password"/>
                <input class="submit" type="submit">
            </form>

            <div class="no-account">
                Already have an account? Log in <a href="{{ route('login') }}">here</a>.
            </div>

            @if ($errors->any())
                <div class="errors">
                    @foreach ($errors->all() as $error)
                        <li>{{ $error }}</li>
                    @endforeach
                </div>
            @endif
        </div>
    @endif
@endsection
