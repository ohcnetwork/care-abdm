# Proving a callback came from ABDM

## In short

- Your callback URL is a public address. Anything on the internet can post to it, and a POST arriving there tells you nothing about who sent it.
- ABDM callbacks declare bearer authentication. The gateway publishes the public keys at `/api/hiecm/gateway/v3/certs`, as a JSON Web Key Set, and that endpoint needs an access token.
- Verify every callback before your handler does any work. Pin the algorithm to `RS256` and fail closed.
- The token arrives in the `Authorization` header as a bearer token.

## Why this one matters

To receive callbacks you register a URL that ABDM can reach. Reachable by ABDM means reachable by everyone, because it is an ordinary address on the public internet.

The callbacks you host carry instructions about a named person's health records: a request to discover what you hold, a [consent artefact](/docs/hiecm/v3/concepts/consent) saying somebody agreed, an instruction to transfer records to a given address. A system that acts on whatever arrives will act on whatever an attacker sends.

ABDM callbacks declare bearer authentication, and the gateway publishes the public keys that verify the token. You fetch the keys once, cache them, and check the signature on every callback before your handler does anything.

Two different signatures

The signature inside a [consent artefact](/docs/hiecm/v3/concepts/consent) is a different thing. It signs the artefact's contents and proves the artefact was not altered. The one on this page signs the delivery and proves who sent it. Verifying one does not verify the other.

## Before you start

You need a callback URL registered with ABDM, and an understanding of why a 200 is not an answer, which is on [how a record travels](/docs/hiecm/v3/concepts/data-flow).

You need an access token for this. The certificates endpoint declares bearer authentication and a required `X-CM-ID` header in the specification.

## Fetch the key set

```bash
curl --request GET \  --url https://dev.abdm.gov.in/api/hiecm/gateway/v3/certs \  --header 'Authorization: Bearer <ACCESS_TOKEN>' \  --header 'REQUEST-ID: <REQUEST_ID>' \  --header 'TIMESTAMP: <TIMESTAMP>' \  --header 'X-CM-ID: sbx'
```

Each key carries a `kid` that identifies it, `kty: RSA`, `use: sig`, and an `alg` the specification gives as `RS256`. The `n` and `e` fields are the RSA modulus and exponent, Base64URL encoded, and some keys also carry `x5c`, a certificate chain.

The same key set is discoverable through the OIDC document at `/api/hiecm/gateway/v3/.well-known/openid-configuration`, which names it in `jwks_uri`. Reading the discovery document first survives the key set moving.

Cache the keys rather than fetching them per callback, and key your cache by `kid`. When a callback presents a `kid` you have not seen, refetch once before rejecting it. That is what key rotation looks like from your side.

Verification is then the ordinary JWT check your library already does: signature against the key named by `kid`, algorithm pinned to `RS256`, and the expiry and issuer claims if the token carries them.

## Which header carries the token

The header is declared

Every webhook definition in the M2 and M3 specifications declares bearer authentication. The token arrives in the `Authorization` header as `Bearer <token>`.

Pin the algorithm to `RS256` when you verify, and reject `none`. A verifier that accepts whatever algorithm the token names accepts a token an attacker signed, and that is a defect in the verifier rather than in ABDM.

## How you know it worked

You can fetch the certificates endpoint and get back a `keys` array whose entries carry `kid`, `kty: RSA` and `use: sig`.

Then, on your own handler, both of these hold:

1. A callback carrying a valid signature is processed, and its `response.requestId` matches the `REQUEST-ID` of a request you sent.
2. The same callback body, replayed with the signature altered by one character, is rejected before your handler reads the payload, and the rejection is logged.

The second is the one worth writing a test for. It is the only one that fails loudly when verification is silently skipped.

## When it goes wrong

**The `kid` is not in your cache.** That is key rotation. Refetch the key set once, then reject if it is still absent, rather than refetching on every callback and handing an attacker a way to make you call the gateway.

**You cannot find a token on the request.** The webhook definitions declare bearer authentication, so read the `Authorization` header. Do not fall back to processing unverified requests while you work it out.

**Verification is skipped under load.** A handler that verifies inside a try block and continues on failure is worse than one that never verified, because it reads as safe. Fail closed.

**Nothing arrives at all**, which is a different problem. See [the callback never arrives](/docs/hiecm/v3/troubleshooting/callback-never-arrives).
