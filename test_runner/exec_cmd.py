import re
import os

from time import sleep
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
  def __init__(self, cmd, working_dir=None, during=None, after=None):
    print("cmd: " + cmd)
    print("working_dir: " + str(working_dir))
    proc = Popen([cmd], cwd=working_dir, shell=True, stderr=PIPE)
    start_new_thread(self.handle_proc, (proc, during, after))
    start_new_thread(self.handle_stderr, (proc.stderr,))

  def handle_proc(self, proc, during, after):
    while proc:
      sleep(1)
      if during: during()
      retcode = proc.poll()
      if retcode is not None:
        if after: after()
        return

  def handle_stderr(self, stderr):
    while True:
      data = os.read(stderr.fileno(), 128*1024)
      if data and data != "":
        print(data)
      else:
        stderr.close()
        return
