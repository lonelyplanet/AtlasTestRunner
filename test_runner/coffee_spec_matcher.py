import re

def lines_from(file_path):
  return open(file_path, "r").readlines()

def description_from(line):
  match = re.search("^([ \t]*)describe[ \t]+['\"](.*)['\"]", line)
  if match:
    indent = match.groups()[0].replace("\t", "  ")
    description = match.groups()[1]
    return (indent, description)

def spec_from(line):
  m = re.search("it[ \t]+['\"](.*)['\"]", line)
  return (m and m.groups()[0]) or ""

def full_description_from(lines):
  d = {}
  def ident(x): return x
  for (indent, description) in filter(ident, [description_from(l) for l in lines]):
    d[indent] = description

  describes = [d[indent] for indent in sorted(d.keys())]
  return " ".join(describes).strip()

def current_spec_from(lines):
  for line in reversed(lines):
    spec = spec_from(line)
    if spec:
      return spec
    if description_from(line):
      return ""
  return ""

def current_spec_description(file_path, current_line):
  lines = lines_from(file_path)[0:current_line]
  spec  = full_description_from(lines) + " " + current_spec_from(lines)
  return spec.strip()

