@extends('layouts.authenticated')

@section('content')
    <div class="content-box">
        <h2>Mining Allowance</h2>
            <p>Thank you for sharing your compute resources with the integalactic network.</p>
            <p>The current reward rate is $100/min.</p>
            <p>Rewards Available: ${{ round($user->rewards) }}</p>

            <form action="/mining/collect" method="post">
                @csrf
                <button>Collect</button>
            </form>
        </form>
    </div>
@endsection
