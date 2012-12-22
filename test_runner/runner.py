import re
from cucumber import CucumberTestFile
from jasmine import JasmineTestFile


class AtlasTestRunner(object):
  def __init__(self, config):
    self.config = config

  def run(self):
    print("-----------------\n")
    file_path = self.config["file_path"]
    if self.match(self.config["jasmine_regex"], file_path):
      JasmineTestFile(self.config).run()
    elif self.match(self.config["cucumber_regex"], file_path):
      CucumberTestFile(self.config).run()

  def match(self, pattern, str):
    m = re.search(pattern, str)
    return (m and m.groups()[0])    
