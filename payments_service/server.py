#! /usr/bin/env python3.6

"""
server.py
Stripe Sample.
Python 3.6 or newer required.
"""
import os
from flask import Flask, redirect, request

import stripe
# This test secret API key is a placeholder. Don't include personal details in requests with this key.
# To see your test secret API key embedded in code samples, sign in to your Stripe account.
# You can also find your test secret API key at https://dashboard.stripe.com/test/apikeys.
stripe.api_key = 'sk_test_51Q5nTOKwSZK9imXGOkCnYUo40Zj36JpDHTfe3ti0GglZCcXZw2AkvvwbXRSZOfloqUWosJf6PxhiIwNndw5wAMhw00qHU5OT9m'

app = Flask(__name__,
            static_url_path='',
            static_folder='public')

YOUR_DOMAIN = 'http://localhost:8001'

@app.route('/create-checkout-session', methods=['POST', "GET"])
def create_checkout_session():
    try:
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
                    'price': 'price_1Q5osbKwSZK9imXG8y6RqVaX',
                    'quantity': 1,
                },
            ],
            mode='subscription',
            success_url=YOUR_DOMAIN + '?success=true',
            cancel_url=YOUR_DOMAIN + '?canceled=true',
        )
        session_id = checkout_session.id
        session_url = checkout_session.url

        # Optional: Return session details in the response
        return {
            "session_id": session_id,
            "session_url": session_url
        }
    except Exception as e:
        return str(e)


if __name__ == '__main__':
    app.run(port=8001)


{
"session_id": "cs_test_a1vXMtV0eOkSHv28wnHphhwSBVWoL2xMAT6JOgygx8TyqEU3ANpzmRYKjw",
"session_url": "https://checkout.stripe.com/c/pay/cs_test_a1vXMtV0eOkSHv28wnHphhwSBVWoL2xMAT6JOgygx8TyqEU3ANpzmRYKjw#fidkdWxOYHwnPyd1blpxYHZxWjA0VDBrUUpOclZfTjxsaF1CVWFUUDU8cTxxUTFSb0BRREgwUEtuZ39LNDdAcjNoSUd2UjZfa0wwYUlmTm9GfGlHTH8xa259N2dQMXFscWc3R1ZAXGRxfENENTV2TlNSdkJXSycpJ2N3amhWYHdzYHcnP3F3cGApJ2lkfGpwcVF8dWAnPyd2bGtiaWBabHFgaCcpJ2BrZGdpYFVpZGZgbWppYWB3dic%2FcXdwYHgl"
}
{
"session_id": "cs_test_a1IEbJro3BSplc2BdiciYM2K7S27524e5FGRtXchOs0UC0iCUt2bc16XMa",
"session_url": "https://checkout.stripe.com/c/pay/cs_test_a1IEbJro3BSplc2BdiciYM2K7S27524e5FGRtXchOs0UC0iCUt2bc16XMa#fidkdWxOYHwnPyd1blpxYHZxWjA0VDBrUUpOclZfTjxsaF1CVWFUUDU8cTxxUTFSb0BRREgwUEtuZ39LNDdAcjNoSUd2UjZfa0wwYUlmTm9GfGlHTH8xa259N2dQMXFscWc3R1ZAXGRxfENENTV2TlNSdkJXSycpJ2N3amhWYHdzYHcnP3F3cGApJ2lkfGpwcVF8dWAnPyd2bGtiaWBabHFgaCcpJ2BrZGdpYFVpZGZgbWppYWB3dic%2FcXdwYHgl"
}