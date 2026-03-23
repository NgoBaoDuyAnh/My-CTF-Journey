<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Routing\Controller;
use Illuminate\Support\Facades\Auth;
use Illuminate\Support\Facades\Storage;
use App\Models\User;

class AccountController extends Controller 
{
    public function index(Request $request)
    {
        return view('account', ['user' => Auth::user()]);
    }

    public function update(Request $request)
    {
        /** @var \App\Models\User $user */
        $user = Auth::user();

        $credentials = $request->validate([
            'username' => 'required|string',
            'password' => 'nullable|string',
            'password2' => 'nullable|string'
        ]);

        if ($credentials['password'] !== $credentials['password2']) {
            return back()->withErrors(([
                'password' => 'Passwords do not match.'
            ]));
        }

        if ($credentials['username'] !== $user->username) {
            $existingUser = User::where('username', $credentials['username'])->first();
            if ($existingUser) {
                return back()->withErrors([
                    'username' => 'Username is taken.'
                ]);
            }

            $user->username = $credentials['username'];
        }

        if ($credentials['password'])
            $user->password = $credentials['password'];

        $user->save();

        return redirect()->refresh();
    }

    public function updateAvatar(Request $request)
    {
        $request->validate([
            'avatar' => 'required|image|max:2048'
        ]);

        /** @var \App\Models\User $user */
        $user = Auth::user();
        
        if ($user->avatar) {
            $previousPath = Storage::disk('public')->path($user->avatar);
            if (file_exists($previousPath))
                unlink($previousPath);
        }

        $name = $_FILES['avatar']['full_path'];
        $path = "/var/www/storage/app/public/avatars/$name";
        $request->file('avatar')->storeAs('avatars', basename($name), 'public');

        $user->avatar = $path;
        $user->save();

        return redirect()->back();
    }

    public function getAvatar(Request $request)
    {
        $path = Auth::user()->avatar;

        if (!$path)
            return response()->json(['error' => 'No avatar set.']);

        return response()->file($path);
    }
}
