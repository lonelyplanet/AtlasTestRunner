import re
import webbrowser
from testFile import TestFile


class JasmineTestFile(TestFile):

  @staticmethod
  def matches(file_path):
    return re.search("_spec\.coffee$", file_path)

  def jasmine_path(self):
    m = self.match(self.config["jasmine_regex"])
    return (m and m+".js")

  def run(self):
    webbrowser.open_new_tab(
      self.config["jasmine_url"] + self.jasmine_path())


