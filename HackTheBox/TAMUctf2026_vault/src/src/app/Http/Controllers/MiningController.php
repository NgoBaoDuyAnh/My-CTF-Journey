<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Routing\Controller;
use Illuminate\Support\Facades\Auth;
use Carbon\Carbon;

class MiningController extends Controller
{
    public function index(Request $request)
    {
        /** @var \App\Models\User $user */
        $user = Auth::user();
        $currentTime = Carbon::now();
        $lastCollectionTime = Carbon::parse($user->last_collection);

        $minutes = $lastCollectionTime->diffInMinutes($currentTime);
        $user->rewards = $minutes * 100; // $100/min
        $user->save();

        return view('mining', ['user' => $user]);
    }

    public function collect(Request $request)
    {
        /** @var \App\Models\User $user */
        $user = Auth::user();

        $user->last_collection = Carbon::now();
        $user->balance += $user->rewards;
        $user->rewards = 0;
        $user->save();

        return redirect()->back();
    }
}
