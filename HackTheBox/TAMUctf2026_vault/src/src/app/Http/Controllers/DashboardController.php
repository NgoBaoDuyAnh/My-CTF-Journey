<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Routing\Controller;
use Illuminate\Support\Facades\Auth;

class DashboardController extends Controller 
{
    public function index(Request $request)
    {
        return view('dashboard', ['user' => Auth::user()]);
    }
}
