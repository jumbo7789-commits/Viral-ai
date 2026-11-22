import unittest
from editing.auto_highlights import SCENE_RE

class HighlightParserTests(unittest.TestCase):
    def test_scene_timestamp_pattern(self):
        text = "pts_time:12.345 pts_time:19.5"
        self.assertEqual(SCENE_RE.findall(text), ["12.345", "19.5"])

if __name__ == "__main__":
    unittest.main()
