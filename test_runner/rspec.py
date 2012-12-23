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
    return self.match(self.config["rspec_regex"])

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
    Exec(cmd, then=self.open_browser(tmpfile))

  def open_browser(self, tmpfile):
    return partial(webbrowser.open_new_tab, "file://" + tmpfile)

  def run_all_tests(self):
    self.run(self.path_to_test_file())

  def run_single_test(self):
    self.run(self.path_to_test_file() + ":" + str(self.config["current_line_number"]))

