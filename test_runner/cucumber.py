import re
import sys
from os.path import dirname

# for Sublime Text 2
sys.path.append(dirname(__file__)+"/../../")

from AtlasTestRunner.test_runner.rspec import RSpecTestFile

class CucumberTestFile(RSpecTestFile):

  @staticmethod
  def matches(file_path):
    return re.search("\.feature$", file_path)

  def path_to_test_file(self):
    return self.extract_file_path(self.config["cucumber_regex"])

  def command(self):
    return self.config["command_prefix"] + "cucumber"

  def options(self):
    opts  = " --format html"
    opts += " --require " + self.config["root_directory"]+"/features"
    opts += " --require " + self.config["root_directory"]+"/features/support"
    opts += " --require " + self.config["root_directory"]+"/features/support/atlas"
    return opts
