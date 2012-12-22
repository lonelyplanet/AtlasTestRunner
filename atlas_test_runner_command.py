import sublime
import sublime_plugin
from atlas_test_runner import AtlasTestRunner

class AtlasTestRunnerCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    runner = AtlasTestRunner(self.view, self.get_config())
    print("\n")
    if runner.jasmine_path():
      runner.run_spec()
    elif runner.feature_path():
      runner.run_feature()

  def get_config(self):
    settings = sublime.load_settings("AtlasTestRunner.sublime-settings")
    return {
      "jasmine_url":    settings.get("jasmine_url"),
      "jasmine_regex":  settings.get("jasmine_regex"),
      "cucumber_regex": settings.get("cucumber_regex"),
      "cucumber_cmd":   settings.get("cucumber_cmd"),
      "current_line_number": self.current_line_number()
    }

  def current_line_number(self):
    char_under_cursor = self.view.sel()[0].a
    return self.view.rowcol(char_under_cursor)[0] + 1

