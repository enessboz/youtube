import importlib.util
import json
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
VIDEO=ROOT/'channels/gestern-gabs-das/videos/001-nachnamen-berufe'
spec=importlib.util.spec_from_file_location('preview',ROOT/'scripts/build_stock_preview.py')
preview=importlib.util.module_from_spec(spec)
spec.loader.exec_module(preview)


class StockPreviewTest(unittest.TestCase):
    def test_caption_split_preserves_every_word_and_two_safe_lines(self):
        text='Die Familiennamen erzählen Geschichten über alte Berufe. Schröder und Schneider gehören ebenfalls zu dieser Geschichte.'
        chunks=preview.split_caption(text)
        self.assertEqual(' '.join(c.replace('\n',' ') for c,_ in chunks),text)
        for caption,count in chunks:
            self.assertLessEqual(count,11)
            self.assertLessEqual(len(caption.split('\n')),2)
            self.assertTrue(all(len(line)<=52 for line in caption.split('\n')))

    def test_timeline_uses_only_reviewed_sources_and_valid_trim_windows(self):
        data=json.loads((VIDEO/'scenes.stock-preview.json').read_text(encoding='utf-8'))
        review={c['filename']:c for c in json.loads((VIDEO/'footage-review.json').read_text(encoding='utf-8'))['clips']}
        last=None
        for scene in data['scenes']:
            self.assertEqual(scene['type'],'clip')
            filename=Path(scene['src']).name
            self.assertNotIn(filename,preview.EXCLUDE)
            self.assertNotEqual(filename,last)
            last=filename
            item=review[filename]
            self.assertTrue(item['accepted'])
            self.assertGreaterEqual(scene['duration_s'],3)
            self.assertLessEqual(scene['duration_s'],6)
            self.assertLessEqual(scene['trim_start_s']+scene['duration_s'],item['duration'])
            self.assertTrue(any(scene['trim_start_s']>=a and scene['trim_start_s']+scene['duration_s']<=b+0.001 for a,b in item['usable_trim_windows_s']))
        actual=sum(round(s['duration_s']*data['fps']) for s in data['scenes'])-(len(data['scenes'])-1)*data['transition_frames']
        self.assertAlmostEqual(actual/data['fps'],data['duration_s'])
        self.assertGreaterEqual(actual/data['fps'],180)
        self.assertLessEqual(actual/data['fps'],300)


if __name__=='__main__':unittest.main()
