import re

def lines_from(file_path):
  return open(file_path, "r").readlines()

def description_from(line):
  match = re.search("^([ \t]*)describe +['\"](.*)['\"]", line)
  if match:
    indent = match.groups()[0].replace("\t", "  ")
    description = match.groups()[1]
    return (indent, description)
  else:
    return ""

def spec_from(line):
  m = re.search("it +['\"](.*)['\"]", line)
  return (m and m.groups()[0]) or ""

def ancestor_describes(lines, current_ndx):
  index = 0
  describe_lines = {}
  while index < current_ndx:
    desc = description_from(lines[index])
    if desc:
      (indent, description)  = desc
      describe_lines[indent] = description
    index += 1

  describes = []
  for indent in sorted(describe_lines.keys()):
    describes.append(describe_lines[indent])
  return " ".join(describes).strip()

def current_spec_line(lines, current_ndx):
  index = current_ndx
  while index > 0:
    line = lines[index]
    if description_from(line):
      return ""
    spec = spec_from(lines[index])
    if spec:
      return spec
    index -= 1
  return ""

def current_spec(file_path, current_ndx):
  lines = lines_from(file_path)
  describe = ancestor_describes(lines, current_ndx)
  spec = describe + " " + current_spec_line(lines, current_ndx)
  return spec.strip()

