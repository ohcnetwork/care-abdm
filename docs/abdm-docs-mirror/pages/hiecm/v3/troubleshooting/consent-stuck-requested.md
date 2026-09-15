# Consent stuck in Requested

You raised a consent request and it has not moved to Granted or Denied. Requested is the starting state of the consent request itself, not of the [consent artefact](/docs/hiecm/v3/getting-started/glossary#consent-artefact) it can produce: the artefact is created only once the patient grants. Nothing has failed yet, the patient has not yet acted, or something kept them from ever seeing it. See [Consent, two objects, not one](/docs/hiecm/v3/concepts/consent#two-objects-not-one) for the full state model.

Before working through the checks, confirm the request itself was accepted, and check its current state rather than only waiting: the [M3 API reference](/docs/hiecm/v3/api/m3) documents the consent request status call.

## Work through these in order

1. **Does the patient's app show the request at all?** The gateway notifies the patient through the ABHA App when a consent request is raised. If the patient uses a third party PHR app instead, that app needs an approved subscription with the gateway to be notified of a new consent request; without one, the request can sit unseen even though it was accepted. Whether the ABHA App itself needs anything set up beyond the patient having an address is not something we have confirmed.
2. **Has the request expired?** A consent request carries a window the requester sets for the patient to respond, separate from how long access lasts once granted. See [Consent](/docs/hiecm/v3/concepts/consent#the-states-a-consent-moves-through) for the two clocks. Running out of the request window moves the state to Expired, not Requested, so checking the current status tells you if this has already happened.
3. **Was it raised against the right ABHA address?** An address that is malformed or does not exist produces an error and the request goes nowhere. A syntactically valid address that belongs to a different real patient will not error at all: the request is delivered and seen, just by the wrong person, not the one you meant. Getting the address right matters more than passing validation.

## How you know it worked

The consent request status reports Granted or Denied rather than Requested. A Granted result also carries the id of at least one consent artefact, and a granted request can produce more than one.

## When it goes wrong

If the patient's app shows the request, it has not expired, and the address is correct, and the state is still Requested after a reasonable wait, this is expected: Requested means the patient has not decided yet, and there is no call that makes them decide faster. If you believe the patient acted and the state did not change, escalate on the [NHA dev forum](https://devforum.abdm.gov.in). Report the consent request id, the `REQUEST-ID` from the init call, the `TIMESTAMP`, and the status response. See [Support](/docs/support) for the full report format.

This symptom can surface as an invalid or non-existent ABHA address on the [error codes reference](/docs/hiecm/v3/reference/error-codes).

[Next Still stuck? Read Consent end to end The full state model, the two clocks, and who holds what.](/docs/hiecm/v3/concepts/consent)
