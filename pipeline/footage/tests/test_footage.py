import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import footage  # noqa: E402


class ParseTest(unittest.TestCase):
    def test_pexels_picks_best_mp4_up_to_1080(self):
        data = {"videos": [{"id": 1, "duration": 12, "url": "u", "user": {"name": "A"}, "image": "t", "video_files": [
            {"file_type": "video/mp4", "width": 3840, "height": 2160, "link": "4k"},
            {"file_type": "video/mp4", "width": 1920, "height": 1080, "link": "hd"},
            {"file_type": "video/webm", "width": 1920, "height": 1080, "link": "webm"},
            {"file_type": "video/mp4", "width": 1280, "height": 720, "link": "sd"}]}]}
        r = footage.parse_pexels(data)
        self.assertEqual(r[0]["file"], "hd")
        self.assertEqual(r[0]["ref"], "pexels:1")

    def test_pixabay_skips_over_1080(self):
        data = {"hits": [{"id": 9, "duration": 8, "pageURL": "p", "user": "B", "videos": {
            "large": {"url": "big", "width": 3840, "height": 2160}, "medium": {"url": "med", "width": 1920, "height": 1080}}}]}
        self.assertEqual(footage.parse_pixabay(data)[0]["file"], "med")


if __name__ == "__main__":
    unittest.main()
