@extends('layouts.authenticated')

@section('content')
    <div class="content-box" style="margin-bottom: 1rem;">
        <h2>Update Account</h2>
        <form method="post">
            @csrf
            <label for="username">Username</label>
            <input id="username" name="username" value={{ $user->username }}>
            <label for="password">Password</label>
            <input id="password" name="password" type="password"/>
            <label for="password2">Confirm Password</label>
            <input id="password2" name="password2" type="password"/>
            <input class="submit" type="submit" value="Save">
        </form>

        @if ($errors->any())
            <div class="errors">
                @foreach ($errors->all() as $error)
                    <li>{{ $error }}</li>
                @endforeach
            </div>
        @endif
    </div>

    <div class="content-box">
        <h2>Transfer Information</h2>
        <label for="account-uuid">Account UUID</label>
        <input class="account-uuid" id="account-uuid" disabled value="{{ $user->uuid }}"/>
    </div>
@endsection
