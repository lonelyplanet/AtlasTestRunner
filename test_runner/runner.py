import re
import sys
from os.path import dirname

# for Sublime Text 2
sys.path.append(dirname(__file__)+"/../../")

from AtlasTestRunner.test_runner.cucumber import CucumberTestFile
from AtlasTestRunner.test_runner.rspec    import RSpecTestFile
from AtlasTestRunner.test_runner.unknown  import UnknownTestFile
from AtlasTestRunner.test_runner.jasmine_coffee  import JasmineCoffeeTestFile

class AtlasTestRunner(object):
  def __init__(self, config):
    self.config = config

  def current_test(self):
    file_path = self.config["file_path"]

    if JasmineCoffeeTestFile.matches(file_path):
      return JasmineCoffeeTestFile(self.config)

    if CucumberTestFile.matches(file_path):
      return CucumberTestFile(self.config)

    if RSpecTestFile.matches(file_path):
      return RSpecTestFile(self.config)

    return UnknownTestFile(self.config)

  def run_all_tests(self):
    self.current_test().run_all_tests()

  def run_single_test(self):
    self.current_test().run_single_test()

