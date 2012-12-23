import re
from cucumber import CucumberTestFile
from jasmine  import JasmineTestFile
from rspec    import RSpecTestFile
from unknown  import UnknownTestFile


class AtlasTestRunner(object):
  def __init__(self, config):
    self.config = config

  def current_test(self):
    file_path = self.config["file_path"]

    if JasmineTestFile.matches(file_path):
      return JasmineTestFile(self.config)

    if CucumberTestFile.matches(file_path):
      return CucumberTestFile(self.config)

    if RSpecTestFile.matches(file_path):
      return RSpecTestFile(self.config)

    return UnknownTestFile(self.config)

  def run(self):
    self.current_test().run()

