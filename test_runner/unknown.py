import sys
from os.path import dirname

# for Sublime Text 2
sys.path.append(dirname(__file__)+"/../../")

from AtlasTestRunner.test_runner.testFile import TestFile

class UnknownTestFile(TestFile):

  def display_unknown_error(self):
    self.config["fn"]["error_message"]("unknown type of testfile:\n\n"+self.config["file_path"])

  def run_all_tests(self):
    self.display_unknown_error()

  def run_single_test(self):
    self.display_unknown_error()

