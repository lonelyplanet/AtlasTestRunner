import unittest
from atlas_test_runner import AtlasTestRunner

class TestAtlasTestRunner(unittest.TestCase):
  def setUp(self):
    global runner
    runner = AtlasTestRunner(self.get_config())

  def get_config(self):
    return eval(open("AtlasTestRunner.sublime-settings", "r").read())

  def test_jasmine_path(self):
    runner.config["file_path"] = "atlas/spec/javascripts/charlie_spec.coffee"
    self.assertEqual(runner.jasmine_path(), "charlie_spec.js")

  def test_feature_path(self):
    runner.config["file_path"] = "/a/features/ui/delete_poi.feature"
    self.assertEqual(runner.feature_path(), "/a/features/ui/delete_poi.feature")

if __name__ == '__main__':
  unittest.main()
