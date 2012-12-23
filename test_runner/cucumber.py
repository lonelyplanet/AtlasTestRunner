import re
import webbrowser
from testFile import TestFile


class CucumberTestFile(TestFile):

  @staticmethod
  def matches(file_path):
    return re.search("\.feature$", file_path)

  def feature_path(self):
    return self.match(self.config["cucumber_regex"])

  def cucumber_cmd(self):
    cmd   = " " + self.config["cucumber_cmd"]
    opts  = " --format html"
    opts += " --require " + self.config["working_dir"]+"/features/support/atlas"
    return "%(cmd)s %(opts)s " % locals()

  def run(self, testfile):
    tmpfile = self.mktmpfile()
    cmd  = self.cucumber_cmd()
    cmd += " --out " + tmpfile
    cmd += " " + testfile
    self.exec_cmd(cmd)
    webbrowser.open_new_tab("file://%s" % tmpfile)

  def run_all_tests(self):
    self.run(self.feature_path())

  def run_single_test(self):
    self.run(self.feature_path() + ":" + str(self.config["current_line_number"]))

