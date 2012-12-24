import re
from cucumber import CucumberTestFile
from rspec    import RSpecTestFile
from unknown  import UnknownTestFile
from jasmine_coffee  import JasmineCoffeeTestFile


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

