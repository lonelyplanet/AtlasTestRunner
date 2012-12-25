import re
import webbrowser
from testFile import TestFile


class RSpecTestFile(TestFile):
  def __init__(self, config):
    self.config = config
    TestFile.__init__(self, config)

  @staticmethod
  def matches(file_path):
    return re.search("_spec\.rb$", file_path)

  def spec_path(self):
    return self.match(self.config["rspec_regex"])

  def rspec_cmd(self):
    cmd   = " " + self.config["rspec_cmd"]
    opts  = " --format html"
    # opts += " --require " + self.config["working_dir"]+"/features/support/atlas"
    return "%(cmd)s %(opts)s " % locals()

  def run(self):
    # TODO: save active file
    print("\n-------------------\n")
    spec_file = self.spec_path()
    tmpfile = self.mktmpfile()
    cmd  = self.rspec_cmd()
    cmd += " --out %(tmpfile)s %(spec_file)s" % locals()
    self.exec_cmd(cmd)
    webbrowser.open_new_tab("file://%s" % tmpfile)


