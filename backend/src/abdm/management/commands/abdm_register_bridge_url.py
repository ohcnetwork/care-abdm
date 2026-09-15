"""
Register the bridge (callback) URL with the ABDM gateway.

The bridge URL is 1 per clientId, not per facility (docs /getting-started/sandbox:
"One URL covers your whole integration"). The value is ABDM_CALLBACK_BASE_URL + "/api/abdm".
Run this after a deploy or after the dev tunnel URL changes, and before the HRP service
registration on the facility setup page.
"""

from django.core.management.base import BaseCommand, CommandError

from abdm.gateway.bridge import BridgeError, bridge_state, callback_url, register_callback_url


class Command(BaseCommand):
    help = "Register ABDM_CALLBACK_BASE_URL/api/abdm as the ABDM bridge callback URL."

    def add_arguments(self, parser):
        parser.add_argument("--dry-run", action="store_true", help="Print the URL. Do not call the gateway.")

    def handle(self, *args, **options):
        try:
            url = callback_url()
        except BridgeError as exc:
            raise CommandError(str(exc)) from exc
        self.stdout.write(f"Bridge URL: {url}")
        if options["dry_run"]:
            return
        try:
            result = register_callback_url()
        except BridgeError as exc:
            raise CommandError(str(exc)) from exc
        self.stdout.write(
            self.style.SUCCESS(f"Registered. HTTP {result['status_code']}, REQUEST-ID {result['request_id']}")
        )
        state = bridge_state()
        bridge = state.get("bridge") or {}
        self.stdout.write(f"Gateway bridge: id={bridge.get('id') or '-'} url={bridge.get('url') or '-'}")
        if state.get("error"):
            self.stdout.write(self.style.WARNING(state["error"]))
