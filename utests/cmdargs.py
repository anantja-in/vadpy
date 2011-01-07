import unittest
import imp
import sys

sys.path.append('../')
from vadpy import VADpy

settings = imp.load_source('settings', '../settings.py')

class TestParser(unittest.TestCase):
    def setUp(self):
        self.settings = imp.load_source('settings', '../settings.py')

    def test_empty_args(self):
        vp = VADpy(self.settings, '')

    def test_signle_sentinel_arg(self):
        vp = VADpy(self.settings, '!')


class TestDBargs(unittest.TestCase):
    def setUp(self):
        self.settings = imp.load_source('settings', '../settings.py')

    def test_gt_dir(self):
        vp = VADpy(self.settings, '! dbelement gt-dir="some_gt_dir"')
        self.assertEqual(vp._elements[0].gt_dir, 'some_gt_dir')
                
if __name__ == '__main__':
    unittest.main()
