# Design M2, linking and sharing

What the integration has to do to the journey around the calls: how many questions a patient is asked, where a failure is shown, and what a screen is forbidden to claim. Every rule below comes from a Catalogue atom, cited at the end.

## The unit of work is an exchange, not a call

### In plain words

Every M2 and M3 call answers twice. Once straight away, saying the request was
accepted, and later on a callback to your own bridge, saying what actually
happened. Do not treat the first as success. It says the request was accepted,
not that anything was linked.

So the request id stops being a log handle and becomes the join key. An
outbound call, the wait, and the callback that answers it are one exchange, and
they should read as one row with a timeline. Shown as three separate lines they
read as noise, and the difference between accepted and done stays invisible,
which is the one thing the interface exists to show.

### What happens

Register the waiter before sending. A callback that arrives before the HTTP
response returns is a race the sandbox eventually wins.

Then hold five outcomes apart. These must not look alike:

| State | Means | Observed |
|---|---|---|
| sent | in the air | |
| accepted, waiting | `202`, nothing back yet | real patient, 340 ms |
| answered | the callback arrived | |
| refused before waiting | a synchronous `400`, nothing was ever pending | fictional patient, 91 ms |
| no answer in the window | accepted, then silence | real patient, 60,000 ms |

The fourth and fifth are the ones implementations collapse into each other. A
refused call closing its waiter through the same function as an answered one
renders a synchronous `400` as a green callback arrived. Fix that in the shared
function rather than at the call sites that reach it.

The fourth outcome is also useful. Generate link token validates the patient
before accepting the request, so an identity nobody holds is refused at once
with `400` and `ABDM-9999`, while a recognised one is accepted with `202` and
answers later. The two are distinguishable at the first response, so only a
recognised patient is worth waiting for. Note the code: `ABDM-9999` is the catch
all, and the message is the only part naming the cause.

No timeout is published for any of these, so the honest words for the fifth
outcome are that nothing arrived in the window you chose.

### How you know it worked

Send one linking call and read one row. It carries the request id, the outbound
call, the elapsed wait, and the callback when it lands, in one timeline.

Send a call for an identity nobody holds. The row shows refused within a few
hundred milliseconds, never shows waiting, and no waiter is left open.

### When it goes wrong

- A synchronous refusal shows as a completed exchange. The refusal path and the
  callback path share the function that closes the waiter.
- A callback cannot be matched to its call. The waiter was registered after
  sending, and the callback won the race.
- Every call is accepted and nothing ever answers. No callback URL is registered
  against the facility id, which is a configuration cause for a runtime symptom.

## Nobody is standing there, so never block and never lose the state

### In plain words

M1's rules do not carry over to M2. There is no patient to spare a question, no
one time password to save, and no screen anybody is looking at. The patient has
left. What there is instead is a call that was accepted and then went quiet, and
a callback that may arrive tomorrow or never.

Two consequences follow, and they are the opposite of how an M1 journey is
built.

### What happens

**Never block.** Linking is several calls, each answered on a callback that may
be a minute away. A button that waits for the outcome is a button that hangs for
sixty seconds and then says nothing useful. Start the work, return at once, and
point at where it can be watched. The desk gets on with the next patient.

**State outlives the session.** Where a link has got to belongs on the record,
not in a page's memory. Reopening the application must show where everything
stands without re-running anything. This is the reverse of M1, where the whole
journey lives and dies inside one person's visit.

**Name the step, not the spinner.** Linking tells a receptionist nothing. These
do:

- Asking ABDM for a link token.
- Asking ABDM for a link token: ABDM accepted it and no answer came back. This
  client has no callback URL registered, so the answer has nowhere to go.
- Asking ABDM for a link token: refused. `ABDM-9999`, user not found.

The second is the interesting one. It names a configuration cause for a runtime
symptom, which is the difference between a receptionist raising a ticket and an
integrator fixing one line of configuration.

### How you know it worked

Start a link and close the page. Reopen the application and the record shows
which step the link reached, and when, without any call being made again.

Press the button that starts linking. It returns immediately and points at where
progress can be watched. It does not sit waiting for a callback.

### When it goes wrong

- The interface hangs for sixty seconds and then reports nothing. Something is
  waiting on the callback inside the request that started the work.
- Reopening the application shows a link as not started when it was started
  yesterday. The state was held in the page rather than on the record.
- A receptionist raises a ticket for what turns out to be a missing callback
  URL. The message named the symptom without naming the configuration cause.

## A refused request is still remembered, so a retry is a duplicate

### In plain words

ABDM records a link token request even when it refuses the patient, and
deduplicates the next identical request against the one it refused. So a retry
inside that window cannot succeed, and its refusal no longer names the original
cause.

The second message says duplicate, which reads as though the first attempt had
worked. It had not.

### What happens

The same request for the same unknown address, sent twice:

| When | Result |
|---|---|
| 14:17:42 | `400`, `ABDM-9999`, user not found |
| 14:18:51, 69 seconds later | `400`, `ABDM-1092`, duplicate link token request |

The length of the deduplication window is not published. It is at least sixty
nine seconds.

So do not offer a button that cannot work. Where a duplicate is the answer,
explain it, and say that the earlier refusal is the one that names the cause.
Point the reader back at the first exchange rather than at the second.

This is the reason the first refusal has to be kept rather than replaced. An
interface that overwrites the last error with the newest one destroys the only
message that explained anything.

### How you know it worked

Send a request that is refused, then send it again inside the window. The
interface shows `ABDM-1092`, does not present it as a new failure, and links
back to the first exchange and its `ABDM-9999`.

The retry control is absent or disabled while the window is open, rather than
present and failing.

### When it goes wrong

- A retry loop runs and every attempt after the first says duplicate. Nothing is
  checking whether a retry can succeed.
- The cause of a failure cannot be found because the newest message replaced it.
  Keep every exchange, and treat the first refusal as the authoritative one.
- A duplicate refusal is read as evidence that the first request succeeded.
  It is not. The first was refused, and ABDM remembered the refusal.

## What the integrator needs on screen, separately from the patient

### In plain words

A desk that talks to ABDM asynchronously cannot be debugged without a view built
for the integrator rather than the receptionist. It is cheap to build and it is
the difference between a fix that takes a minute and one that takes a day.

### What happens

**A live view of every call and callback, grouped by request id**, so an
outbound call, its wait, and the callback answering it read as one exchange with
a timeline.

**Redact by name and length, never by value.** Show that an `Authorization`
header was sent and how long it was. Never its contents. The panel is a browser.

**Show what would be sent, before sending it.** A request preview or a bundle
inspector turns it failed at the far end into something checkable at the desk.

**A readiness check that names what is missing**, and this is where two
configuration failures have to be told apart:

| Missing | Effect | Treat as |
|---|---|---|
| Facility id | the call cannot be sent | blocker, refuse locally |
| Callback URL | the call sends and is accepted, and the answer has nowhere to go | warning, send anyway |

Treating both as blockers is the tempting mistake. Refusing to send when no
callback URL is registered hides exactly the behaviour the panel exists to make
visible. Send, accept, wait, time out, and say why.

Refuse the first locally and name the value. An invented facility id comes back
from ABDM as an entitlement error that reads like a credentials problem, and
sends the integrator to the console instead of to one line of configuration.

Presence is not validity. `X-HIU-ID` is checked for presence rather than
against any registry: absent is refused `401`, and an invented id is accepted
`202`. Anyone testing with a made up id sees acknowledgements that look like
progress, which is why the local check has to be the strict one.

### How you know it worked

Clear the facility id and press the button. The call is refused before anything
is sent, and the message names the configuration value that is absent.

Clear the callback URL and press the same button. The call is sent, accepted,
waits the window, and reports that nothing arrived and why.

Open the panel during a linking run. Each exchange is one row, headers are shown
by name and length, and no header value appears anywhere.

### When it goes wrong

- A token appears in the panel. Redaction is by value rather than by name and
  length. This is a credential leak, not a display bug.
- An integrator is sent to the developer console by an entitlement error. The
  facility id was not checked locally before the call went out.
- Calls are accepted and nothing ever answers, and the panel says only waiting.
  Name the missing callback URL as the cause, rather than leaving the reader
  with a timeout.

## Inbound is a surface, and silence there is a failure state

### In plain words

M2 and M3 are not only things your desk asks ABDM. ABDM asks your desk things
and waits: a discovery request, a link initiation, a link confirmation, a
request for the records a consent covers, and a consent notification.

Four of those five carry no documented payload in the published sources. A
handler written against an assumed shape fails on the first real delivery,
asynchronously, where nobody is watching. And a handler that only logs leaves a
patient's records undiscoverable while appearing to work.

### What happens

Answer the transport quickly and reason afterwards. ABDM is waiting on a `2xx`,
and a handler that thinks before it replies is a handler that times out.

Then give the interface a state for ABDM asked and this desk has not replied.
Not an empty list, and not silence. A named, visible condition, saying what a
correct reply would have been.

Where the payload is undocumented, record the entire body and the entire header
set on the first delivery of each path, before anything tries to read it. That
first delivery is also the only way to answer a question the published sources
do not: which header carries the signed token on an inbound callback. ABDM signs
its callbacks and publishes the keys, and no source names the field carrying the
signature.

Record header names and lengths, never values. The name is the finding. The
value is a credential.

The security rule underneath: a URL reachable by ABDM is reachable by everyone.
A presented signature that fails verification is refused everywhere. An absent
one may be tolerated on a sandbox, and where it is, the record has to be marked
as unverified rather than passed off as genuine.

### How you know it worked

Trigger a discovery against your bridge. The transport is acknowledged inside
the window, and the interface shows the delivery, the reply, and the time
between them.

Take a path you have never received before. The whole body and the whole header
name set are recorded before any code reads a field, so the shape can be learned
from the record rather than guessed.

Leave an inbound request unanswered on purpose. The interface names it as
unanswered rather than showing nothing.

### When it goes wrong

- A patient's records cannot be found from another facility, and nothing looks
  broken. A discovery handler is logging and not replying.
- Deliveries time out under load. Work is being done before the acknowledgement
  rather than after it.
- A handler throws on the first real delivery. It was written against an assumed
  payload, and the body was never recorded whole.

## A care context and its records are one thing

### In plain words

A care context is the visit. The records are what happened at it. Neither is
useful alone.

A bundle nobody can name a care context for cannot be sent. A care context with
nothing behind it is a promise the next discovery cannot keep: another facility
finds the visit, asks for the records, and there are none.

So store them together and show them together.

### What happens

Show the counts that matter to a patient rather than the ones that are easy to
compute: visits opened, documents attached, and visits not yet findable
elsewhere. The third is the one worth surfacing, because it means a record
exists that no other facility can reach.

Validate before storing, not before sending. Refusing to store a bundle the
receiver could not read is cheap. Discovering it after a consent has been served
is not.

Let the desk inspect a bundle before it goes: the profile it claims, the
resources inside it, the attachment type, and whether every reference resolves
within the bundle. The upload itself wants a drop target, a title prefilled from
the filename but editable, and named refusals for type and for size. Show a hash
and a size so a file is identifiable in a list without keeping a second copy of
it.

Write the title for the patient. They read it in their own application months
later, not the receptionist filing it today.

Never log the attachment. It is a patient's record, and it belongs in the bundle
and in the encrypted payload built from it, nowhere else.

### How you know it worked

Open a visit and attach nothing. The interface counts it as a visit not yet
findable elsewhere, rather than as a completed link.

Attach a document and the same count falls by one.

Try to store a bundle whose references do not resolve inside it. Storing is
refused, and the refusal names the reference that pointed outward.

### When it goes wrong

- Another facility discovers a visit and receives nothing. A care context was
  linked with no records behind it.
- A bundle is refused at the far end, asynchronously, with no explanation
  reaching the desk. It was validated before sending rather than before storing.
- A list of visits becomes slow to open. Bundles are being held in the list
  rather than stored separately and read when needed.

## Where these came from

- `hiecm.concept.m2-exchange-not-call`
- `hiecm.concept.m2-never-block-the-desk`
- `hiecm.concept.m2-retry-is-a-duplicate`
- `hiecm.concept.m2-integrator-call-panel`
- `hiecm.concept.m2-inbound-is-a-surface`
- `hiecm.concept.m2-care-context-and-records`
