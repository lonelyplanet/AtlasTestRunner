import re
import webbrowser
from testFile import TestFile


class UnknownTestFile(TestFile):

  def display_unknown_error(self):
    self.config["error_message"]("unknown type of testfile:\n\n"+self.config["file_path"])

  def run(self):
    self.display_unknown_error()

  def run_single_test(self):
    self.display_unknown_error()

