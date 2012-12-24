import re
import webbrowser

from exec_cmd  import Exec
from testFile  import TestFile
from functools import partial

class RSpecTestFile(TestFile):

  @staticmethod
  def matches(file_path):
    return re.search("_spec\.rb$", file_path)

  def path_to_test_file(self):
    return self.extract_file_path(self.config["rspec_regex"])

  def command(self):
    return self.config["rspec_cmd"]

  def options(self):
    return "--format html"

  def run(self, testfile):
    tmpfile = self.mktmpfile()
    cmd  = self.command()
    cmd += " " + self.options()
    cmd += " --out " + tmpfile
    cmd += " " + testfile
    Exec(cmd, 
         working_dir=self.config["working_dir"], 
         during=self.status_message,
         after=self.open_browser(tmpfile))

  def status_message(self):
    set_status  = self.config["set_status"]
    set_timeout = self.config["set_timeout"]
    set_timeout(partial(set_status, "", "running tests..."), 0)

  def open_browser(self, tmpfile):
    return partial(webbrowser.open_new_tab, "file://" + tmpfile)

  def run_all_tests(self):
    self.run(self.path_to_test_file())

  def run_single_test(self):
    self.run(self.path_to_test_file() + ":" + str(self.config["current_line_number"]))

