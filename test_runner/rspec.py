import re
import webbrowser
from testFile import TestFile


class RSpecTestFile(TestFile):

  @staticmethod
  def matches(file_path):
    return re.search("_spec\.rb$", file_path)

  def spec_path(self):
    return self.match(self.config["rspec_regex"])

  def rspec_cmd(self):
    cmd  = " " + self.config["rspec_cmd"]
    opts = " --format html"
    return "%(cmd)s %(opts)s " % locals()

  def run(self, testfile):
    tmpfile = self.mktmpfile()
    cmd  = self.rspec_cmd()
    cmd += " --out " + tmpfile
    cmd += " " + testfile
    self.exec_cmd(cmd)
    webbrowser.open_new_tab("file://%s" % tmpfile)

  def run_all_tests(self):
    self.run(self.spec_path())

  def run_single_test(self):
    self.run(self.spec_path() + ":" + str(self.config["current_line_number"]))

