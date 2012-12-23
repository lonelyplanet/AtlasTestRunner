import re
import os
import tempfile
import commands
import webbrowser

class TestFile(object):
  def __init__(self, config):
    self.config = config
    self.set_working_dir()

  def match(self, pat):
    m = re.search(pat, self.config["file_path"])
    return (m and m.groups()[0])    

  def mktmpfile(self):
    tmpdir  = tempfile.mkdtemp(prefix="AtlasTests")
    tmpfile = tempfile.NamedTemporaryFile(mode="w", prefix="test", suffix='.html', dir=tmpdir, delete=False)
    return tmpfile.name

  def set_working_dir(self):
    working_dir = os.getcwd()

    if self.config.has_key("working_dir"):
      working_dir = self.config["working_dir"]

      if not os.path.exists(working_dir):
        if self.match(working_dir):
          working_dir = self.match(working_dir)
        else:
          working_dir = os.getcwd()

    self.config["working_dir"] = working_dir


