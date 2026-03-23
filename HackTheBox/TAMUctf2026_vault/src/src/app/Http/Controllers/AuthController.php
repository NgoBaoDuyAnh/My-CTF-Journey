<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Auth;
use Illuminate\Support\Facades\Hash;
use Illuminate\Routing\Controller;
use Illuminate\Support\Str;
use Carbon\Carbon;
use App\Models\User;

class AuthController extends Controller 
{
    public function __construct() {
        $this->middleware(function ($request, $next) 
        {
            if (Auth::check())
                return redirect()->route('dashboard');
            return $next($request);
        })->except('logout');
    }

    public function index(Request $request)
    {
        return view('auth', ['type' => $request->path()]);
    }

    public function auth(Request $request)
    {
        if ($request->path() === 'login')
            return $this->login($request);
        return $this->register($request);
    }

    public function logout(Request $request)
    {
        Auth::logout();
        $request->session()->invalidate();
        $request->session()->regenerateToken();
        return redirect()->route('login');
    }

    public function login(Request $request)
    {
        $credentials = $request->validate([
            'username' => 'required|string',
            'password' => 'required|string'
        ]);

        if (Auth::attempt($credentials)) {
            $request->session()->regenerate();
            return redirect()->route('dashboard');
        }

        return back()->withErrors([
            'username' => 'Invalid username or password.'
        ]);
    }

    public function register(Request $request)
    {
        $credentials = $request->validate([
            'username' => 'required|string',
            'password' => 'required|string',
            'password2' => 'required|string'
        ]);

        if ($credentials['password'] !== $credentials['password2']) {
            return back()->withErrors([
                'password' => 'Passwords do not match.'
            ]);
        }

        $existingUser = User::where('username', $credentials['username'])->first();
        if ($existingUser) {
            return back()->withErrors([
                'username' => 'Username is taken.'
            ]);
        }

        User::create([
            'username' => $credentials['username'],
            'uuid' => Str::uuid(),
            'password' => Hash::make($credentials['password']),
            'last_collection' => Carbon::now()
        ]);

        return redirect()->route('login');
    }
}
