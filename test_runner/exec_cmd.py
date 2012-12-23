import re
import os

from time import sleep
from thread import start_new_thread
from subprocess import Popen, PIPE


# see: http://stackoverflow.com/questions/636561/how-can-i-run-an-external-command-asynchronously-from-python
class Exec(object):
  def __init__(self, cmd, working_dir=None, then=None):
    print("cmd: " + cmd)
    print("working_dir: " + working_dir)
    proc = Popen([cmd], cwd=working_dir, shell=True, stderr=PIPE)
    start_new_thread(self.handle_proc, (proc, then))
    start_new_thread(self.handle_stderr, (proc.stderr,))

  def handle_proc(self, proc, then):
    while proc:
      sleep(1)
      retcode = proc.poll()
      if retcode is not None:
        then()
        return

  def handle_stderr(self, stderr):
    while True:
      data = os.read(stderr.fileno(), 128*1024)
      if data != "":
        print(data)
      else:
        stderr.close()
        return
