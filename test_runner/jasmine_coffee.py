import re
import webbrowser

from testFile import TestFile
from coffee_spec_matcher import current_spec_description


class JasmineCoffeeTestFile(TestFile):

  @staticmethod
  def matches(file_path):
    return re.search("_spec\.coffee$", file_path)

  def jasmine_path(self):
    m = self.extract_file_path(self.config["jasmine_coffee_regex"])
    return (m and m+".js")

  def build_url(self):
    return self.config["jasmine_coffee_url"] + self.jasmine_path()

  def current_spec_description(self):
    return current_spec_description(self.config["file_path"], self.config["line_number"])

  def run_all_tests(self):
    webbrowser.open_new_tab(self.build_url())

  def run_single_test(self):
    webbrowser.open_new_tab(self.build_url()+"?spec="+self.current_spec_description())

