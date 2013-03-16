import re
import webbrowser
import sys
from functools import partial
from os.path   import dirname, abspath

# for Sublime Text 2
sys.path.append(dirname(abspath(__file__))+"/../..")

from AtlasTestRunner.test_runner.exec_cmd  import Exec
from AtlasTestRunner.test_runner.testFile  import TestFile

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
    cmd  = self.command()
    cmd += " " + self.options()
    cmd += " --out " + self.tmpfile
    cmd += " " + testfile
    Exec(cmd,
         working_dir=self.config["working_dir"],
         during=self.status_message,
         after=self.open_browser(self.tmpfile),
         config=self.config)

  def status_message(self):
    set_status  = self.config["set_status"]
    set_timeout = self.config["set_timeout"]
    set_timeout(partial(set_status, "", "running tests..."), 0)

  def open_browser(self, tmpfile):
    return partial(webbrowser.open_new_tab, "file://" + tmpfile)

  def run_all_tests(self):
    self.run(self.path_to_test_file())

  def run_single_test(self):
    self.run(self.path_to_test_file() + ":" + str(self.config["line_number"]))

