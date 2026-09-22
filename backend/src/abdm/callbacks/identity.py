"""How a callback is identified for deduplication. Pure functions, no Django imports.

Every callback row carries a unique `idempotency_key` (models.py:146); `receiver.create_callback`
turns the `IntegrityError` on a repeat into `duplicate=True` and the view answers 202 without
dispatching (callbacks/views.py:36-38). What counts as "the same callback" is decided here.

Two rules:

* A callback that answers a call we made is identified by our REQUEST-ID, its `response.requestId`
  and its `transactionId`, plus the raw body. ABDM sends it once per answer.
* A gateway-initiated notification is redelivered until acknowledged, with a fresh REQUEST-ID and
  a fresh `timestamp` each time, so neither the header nor the body identifies it. `IDENTITY_FIELDS`
  names the payload fields that do.
"""

import hashlib

# operation_id -> the body paths that identify the notification.
#
# Only the HIU consent notify is listed: it is the one gateway-initiated callback whose payload is
# fully identified by its own fields. The M2 discovery and link callbacks carry a `transactionId`,
# which is already in the default key, so their redeliveries dedupe on the default rule.
IDENTITY_FIELDS: dict[str, tuple[tuple[str, ...], ...]] = {
    "m3-hiu-consent-notify": (
        ("notification", "consentRequestId"),
        ("notification", "status"),
    ),
}

# operation_id -> (container path, list key, item key): a list whose members widen the identity.
# A REVOKED notify naming 2 artefacts is not the same notification as one naming 1 of them.
IDENTITY_LISTS: dict[str, tuple[tuple[str, ...], str]] = {
    "m3-hiu-consent-notify": (("notification", "consentArtefacts"), "id"),
}


def body_value(parsed: dict, path: tuple[str, ...]) -> str:
    current = parsed
    for part in path:
        if not isinstance(current, dict):
            return ""
        current = current.get(part)
    return str(current or "")


def identity(operation_id: str, parsed: dict) -> str:
    """The stable identity of a gateway-initiated callback, or "" to fall back to the raw body.

    Returns "" when the identifying fields are all empty: keying a malformed notify on an empty
    identity would collapse every such delivery onto one row and lose the evidence.
    """
    paths = IDENTITY_FIELDS.get(operation_id)
    if not paths:
        return ""
    values = [body_value(parsed, path) for path in paths]
    if not any(values):
        return ""
    listing = IDENTITY_LISTS.get(operation_id)
    if listing:
        container_path, item_key = listing
        container = parsed
        for part in container_path[:-1]:
            container = container.get(part) if isinstance(container, dict) else None
        items = container.get(container_path[-1]) if isinstance(container, dict) else None
        if isinstance(items, list):
            # Sorted: ABDM does not promise an order, and an order change is not a new notification.
            values.extend(sorted(str(i.get(item_key)) for i in items if isinstance(i, dict) and i.get(item_key)))
    return "\0".join(values)


def idempotency_key(
    path: str,
    request_id: str,
    response_request_id: str,
    transaction_id: str,
    raw_body: bytes,
    identity_value: str = "",
) -> str:
    h = hashlib.sha256()
    # A callback with a stable identity of its own is keyed on that alone: its REQUEST-ID and body
    # differ on every redelivery, so including them would make each copy look new.
    head = (path, "", "", "") if identity_value else (path, request_id, response_request_id, transaction_id)
    for value in head:
        h.update(value.encode("utf-8"))
        h.update(b"\0")
    h.update(identity_value.encode("utf-8") if identity_value else raw_body)
    return h.hexdigest()
