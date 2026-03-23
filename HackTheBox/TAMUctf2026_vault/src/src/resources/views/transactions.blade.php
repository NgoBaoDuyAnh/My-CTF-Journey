@extends('layouts.authenticated')

@section('content')
    <div class="content-box" style="margin-bottom: 1rem">
        <h2>Transfer Funds</h2>
        <form method="post">
            @csrf
            <label for="recipient">Recipient UUID</label>
            <input id="recipient" name="recipient">
            <label for="amount">Amount</label>
            <input id="amount" name="amount">
            <input class="submit" type="submit" value="Send">
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
        <h2>Transaction History</h2>
        <table class="transaction-table">
            <tr>
                <th>UUID</th>
                <th>Amount</th>
                <th>Time</th>
            </tr>
            @foreach ($transactions as $transaction)
                @if ($transaction->sender === $user->uuid)
                    <tr>
                        <td>{{ $transaction->recipient }}</td>
                        <td>-${{ $transaction->amount }}</td>
                        <td>{{ $transaction->created_at }}</td>
                    </tr>
                @else
                    <tr>
                        <td>{{ $transaction->sender }}</td>
                        <td>${{ $transaction->amount }}</td>
                        <td>{{ $transaction->created_at }}</td>
                    </tr>
                @endif
            @endforeach
        </table>
    </div>
@endsection