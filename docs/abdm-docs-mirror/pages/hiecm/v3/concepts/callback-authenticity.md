# Proving a callback came from ABDM

## In short

- Your callback URL is a public address. Anything on the internet can post to it, and a POST arriving there tells you nothing about who sent it.
- ABDM signs its callbacks. The gateway publishes the public keys at `/api/hiecm/gateway/v3/certs`, as a JSON Web Key Set, and that endpoint needs no token.
- Verify every callback before your handler does any work. Pin the algorithm to `RS256` and fail closed.
- Which header carries the signed token is not published. Log the headers of your first real callback and confirm it.

## Why this one matters

To receive callbacks you register a URL that ABDM can reach. Reachable by ABDM means reachable by everyone, because it is an ordinary address on the public internet.

The callbacks you host carry instructions about a named person's health records: a request to discover what you hold, a [consent artefact](/docs/hiecm/v3/concepts/consent) saying somebody agreed, an instruction to transfer records to a given address. A system that acts on whatever arrives will act on whatever an attacker sends.

ABDM signs the callbacks it sends, and publishes the public keys that verify those signatures. You fetch the keys once, cache them, and check the signature on every callback before your handler does anything.

Two different signatures

The signature inside a [consent artefact](/docs/hiecm/v3/concepts/consent) is a different thing. It signs the artefact's contents and proves the artefact was not altered. The one on this page signs the delivery and proves who sent it. Verifying one does not verify the other.

## Before you start

You need a callback URL registered with ABDM, and an understanding of why a 200 is not an answer, which is on [how a record travels](/docs/hiecm/v3/concepts/data-flow).

You do not need an access token for this. The certificates endpoint declares no security in the specification, which is what you would expect of an endpoint whose whole job is publishing public keys.

## Fetch the key set

```bash
curl --request GET \  --url https://dev.abdm.gov.in/api/hiecm/gateway/v3/certs \  --header 'REQUEST-ID: <REQUEST_ID>' \  --header 'TIMESTAMP: <TIMESTAMP>'
```

Each key carries a `kid` that identifies it, `kty: RSA`, `use: sig`, and an `alg` the specification gives as `RS256`. The `n` and `e` fields are the RSA modulus and exponent, Base64URL encoded, and some keys also carry `x5c`, a certificate chain.

The same key set is discoverable through the OIDC document at `/api/hiecm/gateway/v3/.well-known/openid-configuration`, which names it in `jwks_uri`. Reading the discovery document first survives the key set moving.

Cache the keys rather than fetching them per callback, and key your cache by `kid`. When a callback presents a `kid` you have not seen, refetch once before rejecting it. That is what key rotation looks like from your side.

Verification is then the ordinary JWT check your library already does: signature against the key named by `kid`, algorithm pinned to `RS256`, and the expiry and issuer claims if the token carries them.

## What this documentation cannot yet tell you

The header is not published

The gateway specification says the key set exists and says what it is for. It does not say which header carries the signed token on an inbound callback.

None of the webhook definitions in the M2 or M3 specifications declares a header or a security scheme at all. So the transport is documented and the field that carries it is not.

Two things follow. Confirm the header name against the sandbox before you write the lookup, by logging the full header set of the first real callback you receive. And treat this page as unconfirmed until somebody has done that.

Pin the algorithm to `RS256` when you verify, and reject `none`. A verifier that accepts whatever algorithm the token names accepts a token an attacker signed, and that is a defect in the verifier rather than in ABDM.

## How you know it worked

You can fetch the certificates endpoint and get back a `keys` array whose entries carry `kid`, `kty: RSA` and `use: sig`.

Then, on your own handler, both of these hold:

1. A callback carrying a valid signature is processed, and the `REQUEST-ID` matches a request you sent.
2. The same callback body, replayed with the signature altered by one character, is rejected before your handler reads the payload, and the rejection is logged.

The second is the one worth writing a test for. It is the only one that fails loudly when verification is silently skipped.

## When it goes wrong

**The `kid` is not in your cache.** That is key rotation. Refetch the key set once, then reject if it is still absent, rather than refetching on every callback and handing an attacker a way to make you call the gateway.

**You cannot find a token on the request.** The header is not declared in any specification here, so log every header of a real callback and read what actually arrives. Do not fall back to processing unverified requests while you work it out.

**Verification is skipped under load.** A handler that verifies inside a try block and continues on failure is worse than one that never verified, because it reads as safe. Fail closed.

**Nothing arrives at all**, which is a different problem. See [the callback never arrives](/docs/hiecm/v3/troubleshooting/callback-never-arrives).
