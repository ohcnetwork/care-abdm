from django.apps import AppConfig

PLUGIN_NAME = "abdm"


class AbdmConfig(AppConfig):
    name = PLUGIN_NAME
    verbose_name = "ABDM"

    def ready(self):
        # Care mounts `<plug>.urls` at api/<plug>/ (care/config/urls.py:111-112).
        # Registers Patient.extensions["abdm"] (ADR-004). Identifier configs are DB rows,
        # created lazily by care_seams.ensure_identifier_configs() on first write.
        import abdm.care_seams  # noqa: F401
        import abdm.signals  # noqa: F401  post_save(Patient) → consume extensions.abdm.txn_id
