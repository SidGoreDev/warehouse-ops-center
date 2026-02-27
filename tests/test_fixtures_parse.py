import unittest
from pathlib import Path

from src.parsing import parse_model_output


class TestFixturesParse(unittest.TestCase):
    def test_fixtures_parse(self) -> None:
        root = Path(__file__).resolve().parent.parent
        fx = root / "fixtures" / "raw"
        files = sorted(fx.glob("*.raw.txt"))
        self.assertGreaterEqual(len(files), 4)
        for p in files:
            with self.subTest(p=p.name):
                text = p.read_text(encoding="utf-8")
                think, parsed, json_text = parse_model_output(text)
                self.assertIsNotNone(think)
                self.assertTrue(json_text.startswith("{") or json_text.startswith("["))
                self.assertIsNotNone(parsed)


if __name__ == "__main__":
    unittest.main()
