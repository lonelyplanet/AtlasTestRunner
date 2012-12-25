import webbrowser
from testFile import TestFile


class CucumberTestFile(TestFile):
  def __init__(self, config):
    self.config = config
    TestFile.__init__(self, config)

  def feature_path(self):
    return self.match(self.config["cucumber_regex"])

  def cucumber_cmd(self):
    cmd   = " " + self.config["cucumber_cmd"]
    opts  = " --format html"
    opts += " --require " + self.config["working_dir"]+"/features/support/atlas"
    return "%(cmd)s %(opts)s " % locals()

  def run(self):
    # TODO: save active file
    print("\n-------------------\n")
    feature = self.feature_path()
    tmpfile = self.mktmpfile()
    cmd  = self.cucumber_cmd()
    cmd += " --out %(tmpfile)s %(feature)s" % locals()
    self.exec_cmd(cmd)
    webbrowser.open_new_tab("file://%s" % tmpfile)
    print("done.\n")


