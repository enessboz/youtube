import os
import shutil
import sys
import tempfile
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
import new_video  # noqa: E402


class NewVideoTest(unittest.TestCase):
    def setUp(self):
        self.root = tempfile.mkdtemp()
        shutil.copytree(os.path.join(ROOT, "shared"), os.path.join(self.root, "shared"))
        ch = os.path.join(self.root, "channels", "demo")
        os.makedirs(ch)
        with open(os.path.join(ch, "channel.yaml"), "w") as f:
            f.write("slug: demo\ntarget_minutes: 27  # hedef\n")

    def tearDown(self):
        shutil.rmtree(self.root)

    def test_numbers_increment_and_templates_filled(self):
        a = new_video.create("demo", "ilk", title="İlk Video", root=self.root)
        b = new_video.create("demo", "ikinci", root=self.root)
        self.assertTrue(os.path.basename(a).startswith("001-"))
        self.assertTrue(os.path.basename(b).startswith("002-"))
        brief = open(os.path.join(a, "brief.md"), encoding="utf-8").read()
        self.assertIn("İlk Video", brief)
        self.assertIn("27 dk", brief)
        self.assertNotIn("{{", brief)
        for d in new_video.SUBDIRS:
            self.assertTrue(os.path.isdir(os.path.join(a, d)))

    def test_rejects_bad_slug_and_template_channel(self):
        with self.assertRaises(ValueError):
            new_video.create("demo", "Kötü Slug", root=self.root)
        os.makedirs(os.path.join(self.root, "channels", "_template"))
        with self.assertRaises(FileNotFoundError):
            new_video.create("_template", "x", root=self.root)


if __name__ == "__main__":
    unittest.main()
