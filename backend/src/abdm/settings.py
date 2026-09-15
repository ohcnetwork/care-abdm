"""
Plugin settings, mirroring care_token_display/settings.py.

Resolution order: settings.PLUGIN_CONFIGS["abdm"] → environment → DEFAULTS.
Secrets (client secret) are only ever read from env / PLUGIN_CONFIGS, never
persisted to the database.
"""

import environ
from django.conf import settings
from django.core.signals import setting_changed
from django.dispatch import receiver

env = environ.Env()

PLUGIN_NAME = "abdm"
ENV_PREFIX = "ABDM_"

# Base URLs come from the docs: sandbox gateway https://dev.abdm.gov.in with
# X-CM-ID sbx; ABHA service https://abhasbx.abdm.gov.in/abha/api/v3/
# (/docs/hiecm/v3/getting-started/sandbox).
#
# HSP_URL is the HSP Registry host that serves the HRP service registration
# (`/v4/int/v1/bridges/MutipleHRPAddUpdateServices`). The docs page
# `/api/gateway/endpoints/gateway-register-bridge-services` conflicts with
# itself: the prose gives https://apihspsbx.abdm.gov.in, the curl example gives
# the gateway host. Observed 2026-09-14: the gateway host answers HTTP 503
# "Please make a valid request."; the prose host answers HTTP 200. The prose
# wins (findings.md).
DEFAULTS = {
    "CLIENT_ID": "",
    "CLIENT_SECRET": "",
    "GATEWAY_URL": "https://dev.abdm.gov.in",
    "HSP_URL": "https://apihspsbx.abdm.gov.in",
    "ABHA_URL": "https://abhasbx.abdm.gov.in/abha/api",
    "CM_ID": "sbx",
    "CALLBACK_BASE_URL": "",
    "CALLBACK_SIGNATURE_HEADER": "Authorization",
    "REQUEST_TIMEOUT_SECONDS": 30,
    # Scan and Share counter QR code. The docs say only that the QR code holds a URL with the
    # HIP ID and a context (docs/findings.md). Placeholders: {hip_id} and {context}.
    # Empty = the setup page shows no QR code and asks for the observed format.
    "SHARE_QR_URL_TEMPLATE": "",
}

MANDATORY_SETTINGS = ("CLIENT_ID", "CLIENT_SECRET")


class PluginSettings:
    def __init__(self, plugin_name, defaults=None, import_strings=None, mandatory=None):
        self.plugin_name = plugin_name
        self.defaults = defaults or {}
        self.import_strings = import_strings or ()
        self.mandatory = mandatory or ()
        self._cached_attrs = set()

    @property
    def user_settings(self):
        if not hasattr(self, "_user_settings"):
            self._user_settings = getattr(settings, "PLUGIN_CONFIGS", {}).get(self.plugin_name, {})
        return self._user_settings

    def __getattr__(self, attr):
        if attr not in self.defaults:
            raise AttributeError(f"Invalid setting: '{attr}'")
        try:
            val = self.user_settings[attr]
        except KeyError:
            val = env(f"{ENV_PREFIX}{attr}", default=self.defaults[attr])
            if isinstance(self.defaults[attr], int) and not isinstance(self.defaults[attr], bool):
                val = int(val)
        self._cached_attrs.add(attr)
        setattr(self, attr, val)
        return val

    def validate(self):
        for setting in self.mandatory:
            if not getattr(self, setting):
                raise AttributeError(f"The '{setting}' setting is required.")

    def reload(self):
        for attr in self._cached_attrs:
            delattr(self, attr)
        self._cached_attrs.clear()
        if hasattr(self, "_user_settings"):
            delattr(self, "_user_settings")


plugin_settings = PluginSettings(PLUGIN_NAME, defaults=DEFAULTS, mandatory=MANDATORY_SETTINGS)


@receiver(setting_changed)
def reload_plugin_settings(*args, **kwargs):
    if kwargs["setting"] == "PLUGIN_CONFIGS":
        plugin_settings.reload()
