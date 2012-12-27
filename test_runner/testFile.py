import re
import os
import tempfile

class TestFile(object):
  def __init__(self, config):
    self.config = config
    self.set_working_dir()
    self.setup_tmpfile()

  def extract_file_path(self, pat):
    m = re.search(pat, self.config["file_path"])
    return (m and m.groups()[0])    

  def mktmpfile(self):
    tmpdir  = tempfile.mkdtemp(prefix="AtlasTests")
    tmpfile = tempfile.NamedTemporaryFile(mode="w", prefix="test", suffix='.html', dir=tmpdir, delete=False)
    return tmpfile.name

  def setup_tmpfile(self):
    self.clear_previous_tempfiles()
    self.tmpfile = self.mktmpfile()
    self.config['set_setting']('previous_tempfile', self.tmpfile)

  def clear_previous_tempfiles(self):
    if self.config.has_key('previous_tmpfile'):
      tmpfile = self.config['previous_tmpfile']
      tmpdir = os.path.dirname(tmpfile)
      if os.path.exists(tmpdir):
        os.system("rm -rf "+tmpdir)
      self.config.pop('previous_tmpfile')
      self.config['erase_setting']('previous_tmpfile')

  def set_working_dir(self):
    # default to cwd
    working_dir = os.getcwd()

    if self.config.has_key("working_dir"):
      # working_dir may be an absolute path,
      # a path relative to $HOME,
      # or a regex with which to pull a substring from the current file_path

      working_dir = self.config["working_dir"]
      working_dir = working_dir.replace("$HOME", os.environ["HOME"])

      if not os.path.exists(working_dir):
        if self.extract_file_path(working_dir):
          working_dir = self.extract_file_path(working_dir)
        else:
          working_dir = os.getcwd()

    self.config["working_dir"] = working_dir


