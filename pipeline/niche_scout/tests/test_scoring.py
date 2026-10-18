import datetime as dt
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import scout  # noqa: E402

NOW = dt.datetime(2026, 10, 18, tzinfo=dt.timezone.utc)


def row(views, subs, created="2026-03-01T00:00:00Z", cid="c"):
    return {"video_id": "v", "title": "t", "channel_id": cid, "channel_title": "x",
            "views": views, "subs": subs, "channel_created": created, "duration_s": 600}


class ScoringTest(unittest.TestCase):
    def test_empty(self):
        self.assertEqual(scout.score([], NOW)["score"], 0.0)

    def test_small_channel_outliers_beat_giants(self):
        good = [row(300_000, 5_000, cid=str(i)) for i in range(6)]
        bad = [row(300_000, 5_000_000, created="2015-01-01T00:00:00Z", cid=str(i)) for i in range(6)]
        self.assertGreater(scout.score(good, NOW)["score"], scout.score(bad, NOW)["score"] + 40)

    def test_hidden_subs_not_counted_as_small(self):
        m = scout.score([row(900_000, None)], NOW)
        self.assertEqual(m["small_hits"], 0)

    def test_duration_parse(self):
        self.assertEqual(scout.parse_duration("PT1H2M3S"), 3723)
        self.assertEqual(scout.parse_duration("PT45S"), 45)
        self.assertEqual(scout.parse_duration("garbage"), 0)

    def test_quota_estimate(self):
        c = [{"niche": "a", "queries": ["x", "y"]}]
        self.assertEqual(scout.estimate_quota(c, ["MX", "ES"]), (2 * 100 + 4) * 2)


if __name__ == "__main__":
    unittest.main()
