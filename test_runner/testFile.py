import re
import os
import tempfile

class TestFile(object):
  def __init__(self, config):
    self.config = config
    self.setup_tmpfile()

  def extract_file_path(self, pat, file_path=None):
    if not file_path:
      file_path = self.config["file_path"]
    m = re.search(pat, file_path)
    return (m and m.groups()[0])    

  def mktmpfile(self):
    tmpdir  = tempfile.mkdtemp(prefix="AtlasTests")
    tmpfile = tempfile.NamedTemporaryFile(mode="w", prefix="test", suffix='.html', dir=tmpdir, delete=False)
    return tmpfile.name

  def setup_tmpfile(self):
    self.clear_previous_tempfiles()
    self.tmpfile = self.mktmpfile()
    self.config['fn']['set_setting']('previous_tempfile', self.tmpfile)

  def clear_previous_tempfiles(self):
    if 'previous_tmpfile' in self.config.keys():
      tmpfile = self.config['previous_tmpfile']
      tmpdir = os.path.dirname(tmpfile)
      if os.path.exists(tmpdir):
        os.system("rm -rf "+tmpdir)
      self.config.pop('previous_tmpfile')
      self.config['fn']['erase_setting']('previous_tmpfile')
