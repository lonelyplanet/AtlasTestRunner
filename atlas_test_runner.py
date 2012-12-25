import re
import os
import tempfile
import commands
import webbrowser

class TestFile(object):
  def _match(self, pat):
    m = re.search(pat, self.config["file_path"])
    return (m and m.groups()[0])    

  def _mktmpfile(self):
    tmpdir  = tempfile.mkdtemp(prefix="AtlasTests")
    tmpfile = tempfile.NamedTemporaryFile(mode="w", prefix="test", suffix='.html', dir=tmpdir, delete=False)
    return tmpfile.name

  def _exec(self, cmd):
    print(cmd)
    cmd = "cd "+self._rails_root() + "; " + cmd
    print(commands.getoutput(cmd))
    print("\n")
 
  def _rails_root(self):
    m = re.search("(.*/atlas).*", os.getcwd())
    if not m:
      return ""
    return m.groups()[0]


class JasmineTestFile(TestFile):
  def __init__(self, config):
    self.config = config

  def jasmine_path(self):
    m = self._match(self.config["jasmine_regex"])
    return (m and m+".js")

  def run(self):
    webbrowser.open_new_tab(
      self.config["jasmine_url"] + self.jasmine_path())


class CucumberTestFile(TestFile):
  def __init__(self, config):
    self.config = config

  def feature_path(self):
    return self._match(self.config["cucumber_regex"])

  def _cucumber_cmd(self):
    cmd   = " " + self.config["cucumber_cmd"]
    opts  = " --format html"
    opts += " --require " + self._rails_root()+"/features/support/atlas"
    return "%(cmd)s %(opts)s " % locals()

  def run(self):
    # TODO: save active file
    print("\n-------------------\n")
    feature = self.feature_path()
    tmpfile = self._mktmpfile()
    cmd  = self._cucumber_cmd()
    cmd += " --out %(tmpfile)s %(feature)s" % locals()
    self._exec(cmd)
    webbrowser.open_new_tab("file://%s" % tmpfile)
    print("done.\n")


class AtlasTestRunner(object):
  def __init__(self, config):
    self.config = config

  def run(self):
    print("-----------------\n")
    file_path = self.config["file_path"]
    if self.match(self.config["jasmine_regex"], file_path):
      JasmineTestFile(self.config).run()
    elif self.match(self.config["cucumber_regex"], file_path):
      CucumberTestFile(self.config).run()

  def match(self, pattern, str):
    m = re.search(pattern, str)
    return (m and m.groups()[0])    
