import re
import webbrowser
from rspec import RSpecTestFile


class CucumberTestFile(RSpecTestFile):

  @staticmethod
  def matches(file_path):
    return re.search("\.feature$", file_path)

  def path_to_test_file(self):
    return self.match(self.config["cucumber_regex"])

  def command(self):
    return self.config["cucumber_cmd"]

  def options(self):
    opts  = " --format html"
    opts += " --require " + self.config["working_dir"]+"/features/support/atlas"
    return opts
