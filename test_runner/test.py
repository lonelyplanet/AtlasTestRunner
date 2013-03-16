#!/usr/bin/env python

import os
import tempfile
import unittest
import sys
from os.path import dirname, abspath

# for Sublime Text 2
sys.path.append(dirname(abspath(__file__))+"/../..")

from AtlasTestRunner.test_runner.cucumber import CucumberTestFile
from AtlasTestRunner.test_runner.rspec    import RSpecTestFile
from AtlasTestRunner.test_runner.testFile import TestFile
from AtlasTestRunner.test_runner.jasmine_coffee  import JasmineCoffeeTestFile

def fixture_path(fname):
  return dirname(abspath(__file__))+"/fixtures/"+fname

def plugin_settings_file():
  return dirname(abspath(__file__))+"/../AtlasTestRunner.sublime-settings"

def dummy_fn(x): return None
def dummy_fn2(x, y): return None

def get_config():
  config = eval(open(plugin_settings_file(), "r").read())
  config.pop("working_dir")
  config["file_path"] = "/dummy/file/path"
  config["erase_setting"] = dummy_fn
  config["set_setting"]   = dummy_fn2
  return config

def mktmpfile():
  tmpdir  = tempfile.mkdtemp(prefix="AtlasTests")
  tmpfile = tempfile.NamedTemporaryFile(mode="w", prefix="test", suffix='.html', dir=tmpdir, delete=False)
  return tmpfile.name


class TestTempFiles(unittest.TestCase):
  def setUp(self):
    global test
    config = get_config()
    config["previous_tmpfile"] = mktmpfile()
    self.tmpdir = os.path.dirname(config["previous_tmpfile"])
    test = TestFile(config)

  def testPreviousTempFileDeleted(self):
    self.assertFalse(os.path.exists(self.tmpdir))


class TestJasmineSingle(unittest.TestCase):
  def setUp(self):
    global test
    config = get_config()
    config["file_path"] = fixture_path("poi_spec.coffee")
    test = JasmineCoffeeTestFile(config)

  def testCurrentSpec(self):
    test.config["line_number"] = 29
    self.assertEqual(test.current_spec_description(), "poi #new when created locally assigns the GUID to the ID")

  def testIndentedCurrentSpec(self):
    test.config["line_number"] = 61
    self.assertEqual(test.current_spec_description(), "poi hasNotes when notes is 'the notes' is truthy")

class TestJasmine(unittest.TestCase):
  def setUp(self):
    global test
    config = get_config()
    config["jasmine_coffee_regex"] = "atlas/spec/javascripts/(.*_spec).coffee"
    test = JasmineCoffeeTestFile(config)

  def test_matches(self):
    self.assertTrue(JasmineCoffeeTestFile.matches("atlas/spec/javascripts/charlie_spec.coffee"))
    self.assertFalse(JasmineCoffeeTestFile.matches("arthur/scargill/loves/his.espresso"))

  def test_jasmine_path(self):
    test.config["file_path"] = "atlas/spec/javascripts/charlie_spec.coffee"
    self.assertEqual(test.jasmine_path(), "charlie_spec.js")


class TestCucumber(unittest.TestCase):
  def setUp(self):
    global test
    config = get_config()
    config["cucumber_regex"] = "(features/.*.feature)"
    test = CucumberTestFile(config)

  def test_matches(self):
    self.assertTrue(CucumberTestFile.matches("yet/another/creature.feature"))
    self.assertFalse(CucumberTestFile.matches("hide/it/from/the.teacher"))

  def test_feature_path(self):
    test.config["file_path"] = "/a/features/ui/delete_poi.feature"
    self.assertEqual(test.path_to_test_file(), "features/ui/delete_poi.feature")


class TestRSpec(unittest.TestCase):
  def setUp(self):
    global test
    config = get_config()
    config["rspec_regex"] = "(spec/.*_spec.rb)"
    test = RSpecTestFile(config)

  def test_matches(self):
    self.assertTrue(RSpecTestFile.matches("spics/and/specs_spec.rb"))
    self.assertFalse(RSpecTestFile.matches("rhymes/with_flex.rb"))

  def test_spec_path(self):
    test.config["file_path"] = "/a/spec/hoi/polloi_spec.rb"
    self.assertEqual(test.path_to_test_file(), "spec/hoi/polloi_spec.rb")


class TestWorkingDirectory(unittest.TestCase):
  def setUp(self):
    global config
    config = get_config()

  def test_unspecified_dir(self):
    test = TestFile(config)
    self.assertEqual(test.config["working_dir"], os.getcwd())

  def test_explicit_dir(self):
    test_dir = os.path.dirname(os.getcwd())
    config["working_dir"] = test_dir
    test = TestFile(config)
    self.assertEqual(test.config["working_dir"], test_dir)

  def test_explicit_though_missing_dir(self):
    config["working_dir"] = "/some/enchanted/evening"
    config["file_path"]   = "/someone/chanted/evening"
    test = TestFile(config)
    self.assertEqual(test.config["working_dir"], os.getcwd())

  def test_regex(self):
    config["working_dir"] = "(.*three/coins)"
    config["file_path"] = "/three/coins/in/a/fountain.feature"
    test = TestFile(config)
    self.assertEqual(test.config["working_dir"], "/three/coins")

  def test_unmatched_regex(self):
    config["working_dir"] = "(.*three/coins)"
    config["file_path"]   = "/roman/holiday.feature"
    test = TestFile(config)
    self.assertEqual(test.config["working_dir"], os.getcwd())

if __name__ == '__main__':
  unittest.main()
