@extends('layouts.authenticated')

@section('content')
    <div class="content-box" style="margin-bottom: 1rem">
        <h2>Create Voucher</h2>
        <form method="post">
            @csrf
            <label for="amount">Amount</label>
            <input id="amount" name="amount">
            <input class="submit" type="submit" value="Create">
        </form>

        @if ($errors->any() && $errors->has('amount'))
            <div class="errors">
                @foreach ($errors->all() as $error)
                    <li>{{ $error }}</li>
                @endforeach
            </div>
        @endif
    </div>

    @if (session('voucher'))
        <div class="content-box" style="margin-bottom: 1rem">
            <h2>Voucher</h2>
            <div class="voucher">
                {{ session('voucher')}}
            </div>
        </div>
    @endif

    <div class="content-box"">
        <h2>Redeem Voucher</h2>
        <form action="/vouchers/redeem" method="post">
            @csrf
            <label for="voucher">Voucher</label>
            <input id="voucher" name="voucher">
            <input class="submit" type="submit" value="Redeem">
        </form>

        @if ($errors->any() && $errors->has('voucher'))
            <div class="errors">
                @foreach ($errors->all() as $error)
                    <li>{{ $error }}</li>
                @endforeach
            </div>
        @endif
    </div>
@endsection
