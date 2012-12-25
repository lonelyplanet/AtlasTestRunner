import sublime
import sublime_plugin
from test_runner.runner import AtlasTestRunner


class AtlasTestRunnerCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    config = self.config()
    print("AtlasTestRunner config:")
    print(config)
    AtlasTestRunner(config).run()

  def config(self):
    settings = sublime.load_settings("AtlasTestRunner.sublime-settings")
    # It's a pain having to copy these settings manually,
    # but sublime.settings offers no way to iterate over its' keys,
    # and we're trying to keep sublime-specific classes outside the runner
    # (mainly becuase it helps with testing)
    return {
      "jasmine_url":    settings.get("jasmine_url"),
      "jasmine_regex":  settings.get("jasmine_regex"),
      "cucumber_regex": settings.get("cucumber_regex"),
      "cucumber_cmd":   settings.get("cucumber_cmd"),
      "rspec_regex":    settings.get("rspec_regex"),
      "rspec_cmd":      settings.get("rspec_cmd"),
      "working_dir":    settings.get("working_dir"),
      "file_path":      self.view.file_name(),
      "error_message":  sublime.error_message,
      "message_dialog": sublime.message_dialog,
      "current_line_number": self.current_line_number(),
    }

  def current_line_number(self):
    char_under_cursor = self.view.sel()[0].a
    return self.view.rowcol(char_under_cursor)[0] + 1

