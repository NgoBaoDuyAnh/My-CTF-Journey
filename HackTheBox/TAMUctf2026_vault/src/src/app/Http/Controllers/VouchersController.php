<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Routing\Controller;
use Illuminate\Support\Facades\Auth;
use Illuminate\Contracts\Encryption\DecryptException;
use Carbon\Carbon;

class VouchersController extends Controller
{
    public function index(Request $request)
    {
        return view('vouchers', ['user' => Auth::user()]);
    }

    public function create(Request $request)
    {
        $data = $request->validate([
            'amount' => 'required|integer|min:1'
        ]);

        /** @var \App\Models\User $user */
        $user = Auth::user();
        $amount = (int) $data['amount'];

        if ($user->balance < $amount) {
            return back()->withErrors([
                'amount' => 'Amount is greater than funds available.'
            ]);
        }

        $user->balance -= $amount;
        $user->save();

        $voucher = encrypt([
            'amount' => $amount,
            'created_by' => $user->uuid,
            'created_at' => Carbon::now()
        ]);

        return back()->with('voucher', $voucher);
    }

    public function redeem(Request $request)
    {
        $data = $request->validate([
            'voucher' => 'required|string'
        ]);

        try {
            $voucher = decrypt($data['voucher']);
        } catch (DecryptException $e) {
            return back()->withErrors([
                'voucher' => 'Invalid voucher.'
            ]);
        }

        /** @var \App\Models\User $user */
        $user = Auth::user();
        $user->balance += $voucher['amount'];
        $user->save();

        return redirect()->back();
    }
}
