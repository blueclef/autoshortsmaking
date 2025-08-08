import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from app.services.subtitle import generate_srt, seconds_to_srt_time

class TestSubtitleGenerator(unittest.TestCase):

    def test_seconds_to_srt_time(self):
        """Tests the conversion of seconds to SRT time format."""
        self.assertEqual(seconds_to_srt_time(0), "00:00:00,000")
        self.assertEqual(seconds_to_srt_time(3.5), "00:00:03,500")
        self.assertEqual(seconds_to_srt_time(65.123), "00:01:05,123")
        self.assertEqual(seconds_to_srt_time(3661), "01:01:01,000")

    def test_generate_srt(self):
        """Tests the generation of the full SRT content from scenes."""
        scenes = [
            {"start": 0, "end": 2.5, "text": "Hello world"},
            {"start": 3, "end": 5.75, "text": "This is a test"}
        ]
        srt_content = generate_srt(scenes)
        expected_content = (
            "1\n"
            "00:00:00,000 --> 00:00:02,500\n"
            "Hello world\n"
            "\n"
            "2\n"
            "00:00:03,000 --> 00:00:05,750\n"
            "This is a test\n"
            ""
        )
        self.assertEqual(srt_content, expected_content)

if __name__ == '__main__':
    unittest.main()
