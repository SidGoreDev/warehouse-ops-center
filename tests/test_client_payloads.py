import unittest

from src.client import build_messages_for_video


class TestClientPayloads(unittest.TestCase):
    def test_media_first(self) -> None:
        msgs = build_messages_for_video(prompt_text="hello", video_url="https://example.com/x.mp4")
        self.assertEqual(msgs[0]["role"], "system")
        self.assertEqual(msgs[1]["role"], "user")
        user_parts = msgs[1]["content"]
        self.assertEqual(user_parts[0]["type"], "video_url")
        self.assertIn("url", user_parts[0]["video_url"])
        self.assertEqual(user_parts[1]["type"], "text")


if __name__ == "__main__":
    unittest.main()
