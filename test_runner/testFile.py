import re
import os
import tempfile
import commands
import webbrowser


class TestFile(object):
  def match(self, pat):
    m = re.search(pat, self.config["file_path"])
    return (m and m.groups()[0])    

  def mktmpfile(self):
    tmpdir  = tempfile.mkdtemp(prefix="AtlasTests")
    tmpfile = tempfile.NamedTemporaryFile(mode="w", prefix="test", suffix='.html', dir=tmpdir, delete=False)
    return tmpfile.name

  def exec_cmd(self, cmd):
    print(cmd)
    cmd = "cd "+self.rails_root() + "; " + cmd
    print(commands.getoutput(cmd))
    print("\n")
 
  def rails_root(self):
    m = re.search("(.*/atlas).*", os.getcwd())
    if not m:
      return ""
    return m.groups()[0]


