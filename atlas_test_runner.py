import re
import os
import tempfile
import commands
import webbrowser

class AtlasTestRunner(object):

  def __init__(self, view):
    self.view = view

  def _match(self, pat):
    m = re.search(pat, self.view.file_name())
    return (m and m.groups()[0])    

  def jasmine_path(self):
    m = self._match("atlas/spec/javascripts/(.*_spec).coffee")
    return (m and m+".js")

  def feature_path(self):
    return self._match("(.*/features/.*.feature)")

  def run_spec(self):
    webbrowser.open_new_tab(
      "http://atlas.local/runspec/spec/" + self.jasmine_path())

  def _mktmpfile(self, prefix="test"):
    tmpdir  = tempfile.mkdtemp(prefix="AtlasTests")
    tmpfile = tempfile.NamedTemporaryFile(mode="w", prefix=prefix, suffix='.html', dir=tmpdir, delete=False)
    fname = tmpfile.name
    return fname

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
  
  def _cucumber_cmd(self):
    cmd   = " bundle exec cucumber"
    opts  = " --format html"
    opts += " --require " + self._rails_root()+"/features/support/atlas"
    return "%(cmd)s %(opts)s " % locals()

  def get_current_line_number(self, view):
    char_under_cursor = view.sel()[0].a
    return view.rowcol(char_under_cursor)[0] + 1

  def run_feature(self):
    # TODO: save active file
    print("\n-------------------\n")
    feature = self.feature_path()
    tmpfile = self._mktmpfile()
    cmd  = self._cucumber_cmd()
    cmd += " --out %(tmpfile)s %(feature)s" % locals()
    self._exec(cmd)
    webbrowser.open_new_tab("file://%s" % tmpfile)
    print("done.\n")

