<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Routing\Controller;
use Illuminate\Support\Facades\Auth;
use App\Models\User;
use App\Models\Transaction;

class TransactionsController extends Controller
{
    public function index(Request $request)
    {
        $user = Auth::user();
        $transactions = Transaction::where('sender', $user->uuid)
                                   ->orWhere('recipient', $user->uuid)
                                   ->get();
        return view('transactions', ['user' => $user, 'transactions' => $transactions]);
    }

    public function send(Request $request)
    {   
        $transaction = $request->validate([
            'recipient' => 'required|string',
            'amount' => 'required|integer|min:1'
        ]);

        /** @var \App\Models\User $user */
        $user = Auth::user();
        $recipient = User::where('uuid', $transaction['recipient'])->first();
        $amount = (int) $request['amount'];

        if (!$recipient) {
            return back()->withErrors(([
                'recipient' => 'User does not exist.'
            ]));
        }

        if ($user->balance < $amount) {
            return back()->withErrors(([
                'amount' => 'Amount is greater than funds available.'
            ]));
        }

        $user->balance -= $amount;
        $recipient->balance += $amount;
        $user->save();
        $recipient->save();

        Transaction::create([
            'sender' => $user->uuid,
            'recipient' => $recipient->uuid,
            'amount' => $amount
        ]);

        return redirect()->refresh();
    }
}
