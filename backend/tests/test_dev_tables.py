"""The table registry of the developer explorer (ADR-018) against the models it describes."""

import re
import unittest
from pathlib import Path

from abdm.dev.redact import SECRET_KEYS, _norm
from abdm.dev.table_specs import TABLE_BY_NAME, TABLE_SPECS

MODELS = Path(__file__).resolve().parents[1] / "src" / "abdm" / "models.py"


def _model_fields() -> dict[str, dict[str, str]]:
    """`{model: {field: kind}}` parsed from models.py, without Django."""
    out: dict[str, dict[str, str]] = {}
    current = None
    for line in MODELS.read_text().splitlines():
        m = re.match(r"^class (\w+)\(BaseModel\)", line)
        if m:
            current = m.group(1)
            out[current] = {}
            continue
        m = re.match(r"^    (\w+) = models\.(\w+)\(", line)
        if m and current:
            out[current][m.group(1)] = m.group(2)
    return out


class TableSpecTests(unittest.TestCase):
    def test_every_model_has_1_spec(self):
        models = _model_fields()
        self.assertEqual(sorted(models), sorted(spec["model"] for spec in TABLE_SPECS))
        self.assertEqual(len(TABLE_SPECS), 17)
        self.assertEqual(len(TABLE_BY_NAME), 17)

    def test_every_named_field_exists(self):
        models = _model_fields()
        for spec in TABLE_SPECS:
            fields = models[spec["model"]]
            for group in (
                "list_fields",
                "secret_fields",
                "heavy_fields",
                "request_fields",
                "callback_fields",
                "filters",
            ):
                for name in spec[group]:
                    self.assertIn(name, fields, f"{spec['name']}.{group}: {name}")
            for name in spec["request_fields"] + spec["callback_fields"]:
                self.assertIn(fields[name], ("ForeignKey", "OneToOneField"), f"{spec['name']}: {name}")

    def test_every_secret_column_is_declared(self):
        """A column whose name is a secret key must be in `secret_fields`, so a row never shows it."""
        models = _model_fields()
        for spec in TABLE_SPECS:
            for field, kind in models[spec["model"]].items():
                if kind in ("TextField", "CharField") and _norm(field) in SECRET_KEYS:
                    self.assertIn(field, spec["secret_fields"], f"{spec['name']}.{field}")

    def test_modules_and_titles(self):
        for spec in TABLE_SPECS:
            self.assertIn(spec["module"], ("gateway", "m1", "m2", "m3", "m4"))
            self.assertTrue(spec["title"])
            self.assertTrue(spec["list_fields"])


if __name__ == "__main__":
    unittest.main()
