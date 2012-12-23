import re
from cucumber import CucumberTestFile
from jasmine import JasmineTestFile


class AtlasTestRunner(object):
  def __init__(self, config):
    self.config = config

  def run(self):
    print("-----------------\n")
    file_path = self.config["file_path"]
    
    if JasmineTestFile.matches(file_path):
      JasmineTestFile(self.config).run()

    elif CucumberTestFile.matches(file_path):
      CucumberTestFile(self.config).run()

    else:
      self.config["error_message"]("unknown type of testfile:\n\n"+file_path)

  def match(self, pattern, str):
    m = re.search(pattern, str)
    return (m and m.groups()[0])    
