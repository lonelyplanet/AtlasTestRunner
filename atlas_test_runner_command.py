import sublime
import sublime_plugin
from atlas_test_runner import AtlasTestRunner

class AtlasTestRunnerCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    runner = AtlasTestRunner(self.view)
    print("\n")
    if runner.jasmine_path():
      runner.run_spec()
    elif runner.feature_path():
      runner.run_feature()

