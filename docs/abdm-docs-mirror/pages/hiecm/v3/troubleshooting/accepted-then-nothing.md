# Accepted, then nothing

You started an M2 flow, one or more calls came back accepted, and then it stalled. Discovery and care context linking are chains of several calls with a callback between each pair, and the flow looks broken from the outside whichever link in that chain is missing, so you have to find which one.

Before working through the checks, know which flow you are in. [Discovery](/docs/hiecm/v3/getting-started/glossary#discovery) is whoever asks to read records, in the [HIU](/docs/hiecm/v3/getting-started/glossary#hiu) direction, looking for what your facility holds: a patient's [PHR](/docs/hiecm/v3/getting-started/glossary#phr) app, another facility, an insurer or a referral service. Linking is you attaching a [care context](/docs/hiecm/v3/concepts/linking) to a patient's [ABHA address](/docs/hiecm/v3/getting-started/glossary#abha-address). You also need the `REQUEST-ID` from the call where the chain started: every callback in the chain should carry it, so it is what lets you find where the chain broke.

## Work through these in order

1. **Discovery request.** Your discovery call should produce an inbound discovery request callback to your bridge. If this never arrives, the problem sits upstream of your system entirely; escalate rather than continuing down this list.
2. **Link initiation.** Starting a link should produce an inbound link init callback. If discovery completed but this never arrives, the stall is at the handoff into linking.
3. **Link confirmation.** Do not treat the synchronous acknowledgement to your link request as success. The confirmation arrives as a separate callback to your registered URL, and the care context only becomes visible in the patient's PHR app once it does. See [linking](/docs/hiecm/v3/concepts/linking) for the full sequence.
4. **`REQUEST-ID` reuse.** If you generated the same `REQUEST-ID` for more than one call in the chain, or reused one from an earlier attempt, responses and callbacks can no longer be told apart. Generate a fresh one per call.

Before assuming any step above is genuinely missing, rule out a callback URL problem first: [the callback never arrives](/docs/hiecm/v3/troubleshooting/callback-never-arrives) covers registration and reachability, which is more common than the gateway itself failing to send.

## How you know it worked

For linking, the care context appears when the patient's PHR app runs discovery against your facility, after the link confirm callback reports success. For discovery, your system answers the inbound discovery callback with the care contexts you hold for that patient.

## When it goes wrong

If you have identified which callback in the chain is missing and ruled out a callback URL problem, raise a request on the [support ticketing platform](https://sandboxsupport.abdm.gov.in/). Report which step of the chain stopped, the `REQUEST-ID` from the call that started it, the `TIMESTAMP`, and every response and callback body you did receive up to the point it stalled. See [what to put in a support request](/docs/hiecm/v3/troubleshooting#what-to-put-in-a-support-request) for the full report format.

This symptom can surface as a duplicate or invalid link reference, or a call made out of the logical sequence, both on the [M2 errors reference](/docs/hiecm/v3/api/m2/errors).

[Next Still stuck? Check the M2 user journey Confirm exactly where your call sits in the sequence, and which callback should follow it.](/docs/hiecm/v3/milestones/m2)
