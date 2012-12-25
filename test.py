import unittest
from atlas_test_runner import JasmineTestFile
from atlas_test_runner import CucumberTestFile


def get_config():
  return eval(open("AtlasTestRunner.sublime-settings", "r").read())


class TestJasmineTestFile(unittest.TestCase):
  def setUp(self):
    global test_file
    test_file = JasmineTestFile(get_config())

  def test_jasmine_path(self):
    test_file.config["file_path"] = "atlas/spec/javascripts/charlie_spec.coffee"
    self.assertEqual(test_file.jasmine_path(), "charlie_spec.js")


class TestCucumberTestFile(unittest.TestCase):
  def setUp(self):
    global test_file
    test_file = CucumberTestFile(get_config())

  def test_feature_path(self):
    test_file.config["file_path"] = "/a/features/ui/delete_poi.feature"
    self.assertEqual(test_file.feature_path(), "/a/features/ui/delete_poi.feature")


if __name__ == '__main__':
  unittest.main()
