"""Exceptions a callback handler may raise to tell `tasks.dispatch_callback` what to do."""


class CallbackNotReady(Exception):
    """The callback is well formed, but the row it names does not exist here *yet*.

    ABDM publishes no ordering guarantee between a call's own `on-…` answer and a
    gateway-initiated notification that names the id that answer carries. A consent notify can
    therefore land before `/v3/hiu/consent/request/on-init` has written `consent_request_id`
    (hiu/service.py::handle_on_init), and the same race exists for the M2 link callbacks.

    Raising this asks the task to try again later instead of failing: the row either appears
    between attempts or it never will. Attempts exhausted is not our failure — the callback is
    marked `unhandled` and the operation's give-up hook acknowledges it to ABDM.

    Do NOT raise this for a callback that is simply unroutable (a request deleted with the
    database, a notification meant for another deployment): every attempt will miss, and the
    give-up path is reached the slow way. It costs only the retry window, but it buys nothing.
    """
