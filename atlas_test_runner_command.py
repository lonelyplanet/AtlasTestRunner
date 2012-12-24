import sublime
import sublime_plugin
from test_runner.runner import AtlasTestRunner


class BaseCommand(sublime_plugin.TextCommand):
  def get_config(self):
    settings = sublime.load_settings("AtlasTestRunner.sublime-settings")
    # It's a pain having to copy these settings manually.
    # But sublime.settings offers no way to iterate over its' keys,
    # and we want to keep all sublime-specific classes outside the test_runner
    # (mainly to aid testing)
    return {
      "jasmine_coffee_url":    settings.get("jasmine_coffee_url"),
      "jasmine_coffee_regex": settings.get("jasmine_coffee_regex"),
      "cucumber_regex": settings.get("cucumber_regex"),
      "cucumber_cmd":   settings.get("cucumber_cmd"),
      "rspec_regex":    settings.get("rspec_regex"),
      "rspec_cmd":      settings.get("rspec_cmd"),
      "working_dir":    settings.get("working_dir"),
      "file_path":      self.view.file_name(),
      "set_status":     self.view.set_status,
      "error_message":  sublime.error_message,
      "set_timeout":    sublime.set_timeout,
      "current_line_number": self.current_line_number(),
    }

  def current_line_number(self):
    char_under_cursor = self.view.sel()[0].a
    return self.view.rowcol(char_under_cursor)[0] + 1


class RunAllTests(BaseCommand):
  def run(self, edit):
    self.config = self.get_config()
    print("AtlasTestRunner config:")
    print(self.config)
    AtlasTestRunner(self.config).run_all_tests()


class RunSingleTest(BaseCommand):
  def run(self, edit):
    self.config = self.get_config()
    print("AtlasTestRunner config:")
    print(self.config)
    AtlasTestRunner(self.config).run_single_test()

