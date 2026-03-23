@extends('layouts.authenticated')

@section('content')
    <div class="options">
        <a class="option" href="{{ route('account') }}"">
            <h2>Account</h2>
        </a>

        <a class="option" href="{{ route('transactions') }}">
            <h2>Transactions</h2>
        </a>

        <a class="option" href="{{ route('mining') }}">
            <h2>Mining</h2>
        </a>

        <a class="option" href="{{ route('vouchers') }}">
            <h2>Vouchers</h2>
        </a>
    </div>
@endsection
