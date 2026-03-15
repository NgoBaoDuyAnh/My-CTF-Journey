# Gambling Coin 3 (BKSEC Training 2026)
---

## Overview

The webapp provides us with a dashboard showing our balance, number of bets have been made by us, betting function and a list of users sorted by balance.

![dashboard](assets/dashboard.png)

## Functionality analysis

An endpoint: `/api/bet`: win bet amount or lose the same amount, chances are 50:50

![bet valid](assets/bet.png)

Doesn't allow betting exceeds current balance

![bet invalid](assets/invalid%20bet.png)

`/api/status`: return json-structure list of users with their name and balance and current account information. Server also grants us an auth_token JWT.

![api status](assets/status.png)

## Vulnerability analysis

Decode the JWT token:

![decode jwt](assets/decode%20jwt.png)

Server doesn't use any algorithm to sign the cookie, which is very dangerous, since attacker can forge the cookie and server won't know.

## Exploitation

Let forge a jwt with username of highest balance: **hay_nuoi_toi**

![forge jwt](assets/forge%20jwt.png)

Paste the forge jwt into **authe_token*** and refresh:

![fake user](assets/fake%20success.png)

Bet for some times to get more than 1000 coins

![bet](assets/flag.png)

> Flag: ***BKSEC{jwt_none_forget_4c3b2a1f_d815d40ca87e485b}***