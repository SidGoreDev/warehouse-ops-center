import unittest

from src.parsing import extract_think, extract_json_text, json_loads_with_repairs, parse_mmssff_to_seconds


class TestParsing(unittest.TestCase):
    def test_extract_think(self) -> None:
        s = "x\n<think>\nhello\n</think>\n{ \"a\": 1 }"
        self.assertEqual(extract_think(s), "hello")

    def test_extract_json_after_think(self) -> None:
        s = "<think>r</think>\n\n{ \"a\": 1, \"b\": [2,3] }\ntrailer"
        self.assertEqual(extract_json_text(s), '{ "a": 1, "b": [2,3] }')

    def test_json_repairs_trailing_comma(self) -> None:
        s = '{ "a": 1, }'
        obj = json_loads_with_repairs(s)
        self.assertEqual(obj["a"], 1)

    def test_parse_mmssff(self) -> None:
        self.assertAlmostEqual(parse_mmssff_to_seconds("01:02.50"), 62.5, places=6)


if __name__ == "__main__":
    unittest.main()
