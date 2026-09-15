# The callback never arrives

You made a call, it came back with a 202 or a 200, and nothing else has happened since. This is a common report in [HIE-CM](/docs/hiecm/v3/getting-started/glossary#hie-cm) integration. The checks below are in the order we recommend, not a record of how often each has turned out to be the actual cause.

That early response only means the [NHA](/docs/hiecm/v3/getting-started/glossary#nha) gateway accepted your request. In M2 and M3 the real answer arrives later, as a POST from the gateway to a URL you registered in advance. See [the gateway](/docs/hiecm/v3/concepts/gateway) for why this is the normal shape of these flows, and the [API reference](/docs/hiecm/v3/api), where each call names the callback it produces.

## Work through these in order

1. **Is the callback URL registered with the gateway?** Confirm it with the [update bridge callback URL](/docs/hiecm/v3/api/gateway/endpoints/gateway-update-bridge-url) call. Setting a URL in a console once is not the same as confirming the gateway has it.
2. **Is that URL reachable from the public internet over HTTPS?** ABDM posts to it from outside your network. A URL that only answers on your local machine or behind a VPN will never receive anything, and the original call gives you no signal that this is wrong.
3. **Did the request expire before the other party answered?** How long a request stays live before ABDM gives up is not documented yet. If you have waited what feels like a long time, say so when you escalate rather than assuming a fixed window.
4. **Is your endpoint returning a non success status?** A handler that errors, times out, or is slow is a real problem. Whether and when delivery attempts stop is not documented yet. Deliveries can repeat, so your handler has to treat every one as possibly a retry of one it already handled. Respond quickly with a success status even before you have finished processing the callback body.

## How you know it worked

Your handler receives a POST at your registered URL, carrying the exact `REQUEST-ID` you generated for the original call. Until you have observed that once, the callback path is unproven, even if the registration call itself succeeded.

## When it goes wrong

If all four checks pass and the callback still has not arrived, escalate on the [developer forum](https://devforum.abdm.gov.in). Report the API you called, the `REQUEST-ID`, the `TIMESTAMP`, and the response you got. See [Support](/docs/support) for the full report format.

This symptom can surface as [ABDM-9999](/docs/hiecm/v3/reference/error-codes), the catch-all for a failure the gateway does not explain further.

[Next Still stuck? Check the M2 user journey Confirm which step of the sequence your call sits in, so you know which callback should follow it.](/docs/hiecm/v3/milestones/m2)
