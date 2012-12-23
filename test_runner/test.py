#!/usr/bin/env python

import os
import unittest
from cucumber import CucumberTestFile
from jasmine  import JasmineTestFile
from testFile import TestFile


def get_config():
  return {
    "jasmine_url":    "http://atlas.local/runspec/spec/",
    "jasmine_regex":  "atlas/spec/javascripts/(.*_spec).coffee",
    "cucumber_regex": "(.*/features/.*.feature)",
    "cucumber_cmd":   "bundle exec cucumber",
    "file_path":      "/dummy/file/path"
  }


class TestJasmineTestFile(unittest.TestCase):
  def setUp(self):
    global test_file
    test_file = JasmineTestFile(get_config())

  def test_matches(self):
    self.assertTrue(JasmineTestFile.matches("atlas/spec/javascripts/charlie_spec.coffee"))
    self.assertFalse(JasmineTestFile.matches("arthur/scargill/loves/his.espresso"))

  def test_jasmine_path(self):
    test_file.config["file_path"] = "atlas/spec/javascripts/charlie_spec.coffee"
    self.assertEqual(test_file.jasmine_path(), "charlie_spec.js")


class TestCucumberTestFile(unittest.TestCase):
  def setUp(self):
    global test_file
    test_file = CucumberTestFile(get_config())

  def test_matches(self):
    self.assertTrue(CucumberTestFile.matches("yet/another/creature.feature"))
    self.assertFalse(CucumberTestFile.matches("hide/it/from/the.teacher"))

  def test_feature_path(self):
    test_file.config["file_path"] = "/a/features/ui/delete_poi.feature"
    self.assertEqual(test_file.feature_path(), "/a/features/ui/delete_poi.feature")


class TestWorkingDirectory(unittest.TestCase):
  def setUp(self):
    global config
    config = get_config()

  def test_unspecified_dir(self):
    test_file = TestFile(config)
    self.assertEqual(test_file.config["working_dir"], os.getcwd())

  def test_explicit_dir(self):
    test_dir = os.path.dirname(os.getcwd())
    config["working_dir"] = test_dir
    test_file = TestFile(config)
    self.assertEqual(test_file.config["working_dir"], test_dir)

  def test_explicit_though_missing_dir(self):
    config["working_dir"] = "/some/enchanted/evening"
    config["file_path"]   = "/someone/chanted/evening"
    test_file = TestFile(config)
    self.assertEqual(test_file.config["working_dir"], os.getcwd())

  def test_regex(self):
    config["working_dir"] = "(.*three/coins)"
    config["file_path"] = "/three/coins/in/a/fountain.feature"
    test_file = TestFile(config)
    self.assertEqual(test_file.config["working_dir"], "/three/coins")

  def test_unmatched_regex(self):
    config["working_dir"] = "(.*three/coins)"
    config["file_path"]   = "/roman/holiday.feature"
    test_file = TestFile(config)
    self.assertEqual(test_file.config["working_dir"], os.getcwd())

if __name__ == '__main__':
  unittest.main()
