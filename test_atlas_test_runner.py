import unittest
from atlas_test_runner import AtlasTestRunner

class MockView(object):
  def __init__(self):
    self.fname = "atlas/spec/javascripts/charlie_spec.coffee"

  def file_name(self):
    return self.fname

class TestAtlasTestRunner(unittest.TestCase):
  def setUp(self):
    global runner
    runner = AtlasTestRunner(MockView())

  def test_jasmine_path(self):
    runner.view.fname = "atlas/spec/javascripts/charlie_spec.coffee"
    self.assertEqual(runner.jasmine_path(), "charlie_spec.js")

  def test_feature_path(self):
    runner.view.fname = "/a/features/ui/delete_poi.feature"
    self.assertEqual(runner.feature_path(), "/a/features/ui/delete_poi.feature")

if __name__ == '__main__':
  unittest.main()
