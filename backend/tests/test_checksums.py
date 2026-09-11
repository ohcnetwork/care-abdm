import unittest

from abdm.abha.checksums import is_valid_aadhaar, is_valid_abha_number


def luhn_check_digit(prefix: str) -> str:
    total = 0
    for i, ch in enumerate(reversed(prefix + "0")):
        digit = int(ch)
        if i % 2 == 1:
            digit *= 2
            if digit > 9:
                digit -= 9
        total += digit
    return str((10 - (total % 10)) % 10)


_D = [
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
    [1, 2, 3, 4, 0, 6, 7, 8, 9, 5],
    [2, 3, 4, 0, 1, 7, 8, 9, 5, 6],
    [3, 4, 0, 1, 2, 8, 9, 5, 6, 7],
    [4, 0, 1, 2, 3, 9, 5, 6, 7, 8],
    [5, 9, 8, 7, 6, 0, 4, 3, 2, 1],
    [6, 5, 9, 8, 7, 1, 0, 4, 3, 2],
    [7, 6, 5, 9, 8, 2, 1, 0, 4, 3],
    [8, 7, 6, 5, 9, 3, 2, 1, 0, 4],
    [9, 8, 7, 6, 5, 4, 3, 2, 1, 0],
]
_P = [
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
    [1, 5, 7, 6, 2, 8, 3, 0, 9, 4],
    [5, 8, 0, 3, 7, 9, 6, 1, 4, 2],
    [8, 9, 1, 6, 0, 4, 3, 5, 2, 7],
    [9, 4, 5, 3, 1, 2, 6, 8, 7, 0],
    [4, 2, 8, 6, 5, 7, 3, 9, 0, 1],
    [2, 7, 9, 3, 8, 0, 6, 4, 1, 5],
    [7, 0, 4, 6, 9, 1, 3, 2, 5, 8],
]
_INV = [0, 4, 3, 2, 1, 5, 6, 7, 8, 9]


def verhoeff_check_digit(prefix: str) -> str:
    c = 0
    for i, ch in enumerate(reversed(prefix)):
        c = _D[c][_P[(i + 1) % 8][int(ch)]]
    return str(_INV[c])


class ChecksumTests(unittest.TestCase):
    def test_abha_number_luhn_accepts_synthetic_valid_number(self):
        prefix = "1234567890123"
        self.assertTrue(is_valid_abha_number(prefix + luhn_check_digit(prefix)))

    def test_abha_number_luhn_rejects_bad_shapes(self):
        valid = "1234567890123" + luhn_check_digit("1234567890123")
        wrong_digit = valid[:-1] + str((int(valid[-1]) + 1) % 10)
        self.assertFalse(is_valid_abha_number(wrong_digit))
        self.assertFalse(is_valid_abha_number(valid[:-1]))
        self.assertFalse(is_valid_abha_number(valid[:-1] + "x"))

    def test_aadhaar_verhoeff_accepts_synthetic_valid_number(self):
        prefix = "23456789012"
        self.assertTrue(is_valid_aadhaar(prefix + verhoeff_check_digit(prefix)))

    def test_aadhaar_verhoeff_rejects_bad_shapes(self):
        valid = "23456789012" + verhoeff_check_digit("23456789012")
        wrong_digit = valid[:-1] + str((int(valid[-1]) + 1) % 10)
        self.assertFalse(is_valid_aadhaar(wrong_digit))
        self.assertFalse(is_valid_aadhaar(valid[:-1]))
        self.assertFalse(is_valid_aadhaar(valid[:-1] + "x"))
        self.assertFalse(is_valid_aadhaar("0" + valid[1:]))


if __name__ == "__main__":
    unittest.main()
