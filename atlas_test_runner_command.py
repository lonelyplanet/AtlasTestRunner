import os
import sys
import sublime
import sublime_plugin

from os.path import dirname

# for Sublime Text 2
sys.path.append(dirname(__file__)+"/../")

from AtlasTestRunner.test_runner.runner import AtlasTestRunner

class BaseCommand(sublime_plugin.TextCommand):
  def get_config(self):
    settings = sublime.load_settings("AtlasTestRunner.sublime-settings")
    # It's a pain having to copy these settings manually,
    # but sublime.settings has no way to iterate over its' keys.
    config = {
      "jasmine_coffee_url":   settings.get("jasmine_coffee_url"),
      "jasmine_coffee_regex": settings.get("jasmine_coffee_regex"),
      "cucumber_regex": settings.get("cucumber_regex"),
      "cucumber_cmd":   settings.get("cucumber_cmd"),
      "rspec_regex":    settings.get("rspec_regex"),
      "rspec_cmd":      settings.get("rspec_cmd"),
      "root_directory": self.root_directory(),
      "file_path":      self.view.file_name(),
      "line_number":    self.line_number(),
      "command_prefix": self.command_prefix(),
      "fn":             {
        "set_status":     self.view.set_status,
        "erase_setting":  self.erase_setting,
        "set_setting":    self.set_setting,
        "error_message":  sublime.error_message,
        "set_timeout":    sublime.set_timeout
      }
    }
    self.log(config)
    return config

  def log(self, config):
    print("AtlasTestRunner config:")
    print("-----------------------")
    max_key_len = max(map(len, config.keys()))
    for k in sorted(config.keys()):
      if k != "fn":
        key = k.ljust(max_key_len)
        print("%s: %s" % (key, config[k]))
    print("-----------------------")

  def root_directory(self):
    try:
      return sublime.active_window().project_data()['folders'][0]['path']
    except:
      return sublime.active_window().folders()[0]

  def command_prefix(self):
    rvm_prefix = os.path.expanduser("~/.rvm/bin/rvm-auto-ruby")
    if os.path.exists(rvm_prefix):
      return rvm_prefix + " -S "
    return ""

  def erase_setting(self, setting):
    settings = sublime.load_settings("AtlasTestRunner.sublime-settings")
    settings.erase(setting)
    sublime.save_settings("AtlasTestRunner.sublime-settings")

  def set_setting(self, name, value):
    settings = sublime.load_settings("AtlasTestRunner.sublime-settings")
    settings.set(name, value)
    sublime.save_settings("AtlasTestRunner.sublime-settings")

  def line_number(self):
    char_under_cursor = self.view.sel()[0].a
    return self.view.rowcol(char_under_cursor)[0] + 1

  def view_is_saved(self):
    if not self.view.is_dirty():
      return True
    sublime.message_dialog("Please save this test before running.")
    return False


class RunAllTests(BaseCommand):
  def run(self, edit):
    if self.view_is_saved():
      AtlasTestRunner(self.get_config()).run_all_tests()


class RunSingleTest(BaseCommand):
  def run(self, edit):
    if self.view_is_saved():
      AtlasTestRunner(self.get_config()).run_single_test()


