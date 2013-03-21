import re
import sys
import webbrowser

from functools import partial
from os.path   import dirname

# for Sublime Text 2
sys.path.append(dirname(__file__)+"/../../")

from AtlasTestRunner.test_runner.exec_cmd import Exec
from AtlasTestRunner.test_runner.testFile import TestFile
from AtlasTestRunner.test_runner.spinner  import StatusSpinner

class RSpecTestFile(TestFile):

  @staticmethod
  def matches(file_path):
    return re.search("_spec\.rb$", file_path)

  def path_to_test_file(self):
    return self.extract_file_path(self.config["rspec_regex"])

  def command(self):
    return self.config["command_prefix"] + self.config["rspec_cmd"]

  def options(self):
    return "--format html"

  def run(self, testfile):
    self.set_status  = self.config["fn"]["set_status"]
    self.set_timeout = self.config["fn"]["set_timeout"]
    self.spinner     = StatusSpinner()
    cmd  = self.command()
    cmd += " " + self.options()
    cmd += " --out " + self.tmpfile
    cmd += " " + testfile
    Exec(cmd,
         working_dir=self.config["root_directory"],
         during=self.during,
         after=self.after,
         config=self.config)

  def during(self):
    self.set_timeout(partial(self.set_status, "AtlasTestRunner", "running tests:"+self.spinner.status()), 0)

  def after(self):
    self.set_timeout(partial(self.set_status, "AtlasTestRunner", ""), 0)
    self.set_timeout(partial(webbrowser.open_new_tab, "file://" + self.tmpfile), 0)

  def run_all_tests(self):
    self.run(self.path_to_test_file())

  def run_single_test(self):
    self.run(self.path_to_test_file() + ":" + str(self.config["line_number"]))

