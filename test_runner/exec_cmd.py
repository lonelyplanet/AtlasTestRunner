import re
import os
import sys

from time       import sleep
from os.path    import dirname
from subprocess import Popen, PIPE

try:
  # Sublime Text 2
  from thread import start_new_thread
except ImportError:
  # Sublime Text 3
  from threading import Thread
  def start_new_thread(fn, args):
    Thread(target=fn, args=args).start()

# see: http://stackoverflow.com/questions/636561/how-can-i-run-an-external-command-asynchronously-from-python
class Exec(object):
  def __init__(self, cmd, working_dir=None, during=None, after=None, config=None):
    print("running cmd: " + cmd)
    print("working dir: " + str(working_dir))
    self.config = config
    self.during = during
    self.after  = after
    self.error_count = 0
    proc = Popen([cmd], cwd=working_dir, shell=True, stderr=PIPE)
    start_new_thread(self.handle_proc, (proc,))
    start_new_thread(self.handle_stderr, (proc.stderr,))

  def handle_proc(self, proc):
    while proc:
      sleep(1)
      if self.during: self.during()
      retcode = proc.poll()
      if retcode is not None:
        if self.after: self.after()
        return

  def handle_stderr(self, stderr):
    while True:
      data = os.read(stderr.fileno(), 128*1024)
      if data and data != "":
        print(data)
        self.show_error(data)
      else:
        stderr.close()
        return

  def show_error(self, text):
    if not self.config: return
    # This might be expressed a little better. However...
    # 1st time through, stderr holds the location in code
    # 2nd time through, stderr holds the stacktrace
    # and only the stacktrace holds a meaningful error message
    self.error_count += 1
    if self.error_count == 2:
      try:
        message = text.split("\n")[0]
        if message.startswith(":"):
          message = message[1:]
        message = message.strip()
        if not "deprecated" in message:
          self.config["error_message"](message)
      except Exception as ex:
        print(ex)
