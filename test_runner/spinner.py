# encoding: UTF-8

STEPS = ['|', '||',  '|||', '|/|', '|-|', '|\|', '|||', '|/|', '|-|', '|\|', '||']

class StatusSpinner(object):
  def __init__(self):
    self.ndx = -1

  def status(self):
    self.ndx += 1
    if self.ndx >= len(STEPS): self.ndx = 0
    return STEPS[self.ndx]
  