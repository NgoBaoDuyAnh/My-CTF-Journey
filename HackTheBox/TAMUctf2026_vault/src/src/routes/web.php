<?php

use Illuminate\Support\Facades\Route;
use App\Http\Controllers\AuthController;
use App\Http\Controllers\DashboardController;
use App\Http\Controllers\AccountController;
use App\Http\Controllers\MiningController;
use App\Http\Controllers\VouchersController;
use App\Http\Controllers\TransactionsController;

Route::middleware(['auth'])->group(function() {
    Route::get('/', [DashboardController::class, 'index'])->name('dashboard');
    Route::get('/account', [AccountController::class, 'index'])->name('account');
    Route::get('/mining', [MiningController::class, 'index'])->name('mining');
    Route::get('/vouchers', [VouchersController::class, 'index'])->name('vouchers');
    Route::get('/transactions', [TransactionsController::class, 'index'])->name('transactions');
    Route::get('/avatar', [AccountController::class, 'getAvatar']);

    Route::post('/account', [AccountController::class, 'update']);
    Route::post('/account/avatar', [AccountController::class, 'updateAvatar']);
    Route::post('/mining/collect', [MiningController::class, 'collect']);
    Route::post('/transactions', [TransactionsController::class, 'send']);
    Route::post('/vouchers', [VouchersController::class, 'create']);
    Route::post('/vouchers/redeem', [VouchersController::class, 'redeem']);
});

Route::get('/login', [AuthController::class, 'index'])->name('login');
Route::get('/register', [AuthController::class, 'index'])->name('register');
Route::get('/logout', [AuthController::class, 'index'])->name('logout');

Route::post('/login', [AuthController::class, 'auth']);
Route::post('/register', [AuthController::class, 'register']);

Route::delete('/logout', [AuthController::class, 'logout']);
