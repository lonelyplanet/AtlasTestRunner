import webbrowser
from testFile import TestFile


class JasmineTestFile(TestFile):
  def __init__(self, config):
    self.config = config

  def jasmine_path(self):
    m = self.match(self.config["jasmine_regex"])
    return (m and m+".js")

  def run(self):
    webbrowser.open_new_tab(
      self.config["jasmine_url"] + self.jasmine_path())


