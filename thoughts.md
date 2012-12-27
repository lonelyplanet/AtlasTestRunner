

* The Python Console within Sublime (`` Ctrl-` ``) is your friend. You can run commands interactively, and output Python's print() command from your code.

* If the plugin appears to have loaded but doesn't run, check your syntax (python source, object-literals and settings files). Syntax errors leave no trace if they break the plugin when loading.

* Sublime will try to re-load your plugin when files change. This can help with small edits or the tweaking of settings files, but be careful: re-loading can be unreliable. After any serious change, a quit and restart is best, making sure to clear out any python bytecode files (`*.pyc`). 
As always, if you catch yourself repeating tasks, automate them:

```shell
    #!/bin/sh

    PLUGIN_DIR=`dirname $0`
    find $PLUGIN_DIR -iname \*.pyc | xargs rm

    subl -n $PLUGIN_DIR
    subl -n $HOME/projects/my/test/project
```

* Try to keep your plugin de-coupled from Sublime. Even though plugins have to extend one of Sublime's Command classes, you can write a wrapper Command that just gathers configuration settings. These settings (including any Sublime callbacks you need) can be passed as a config object to your plugin logic, which can then be mocked by tests. Your classes will run independently, perhaps in a test runner, and you'll gain access to the pydb command-line debugger (since pydb won't work within a Sublime context).

* Any long-running code should be spun off in a separate thread to keep from blocking Sublime. The Default plugin has a comprehensive class (ExecCommand) to run code asynchronously, though for a simpler alternative try `subprocess.Popen`, passing a handler (stderr and/or stdout) to `thread.start_new_thread` :

```python
    from subprocess import Popen, PIPE
    from thread import start_new_thread

    class Exec(object):
      def __init__(self, cmd, working_dir):
        proc = Popen([cmd], cwd=working_dir, shell=True, stdout=None, stderr=PIPE)
        start_new_thread(self.handle_stderr, (proc.stderr,))

      def handle_stderr(self, stderr):
        while True:
          data = os.read(stderr.fileno(), 128*1024)
          if data != "":
            print(data)
          else:
            stderr.close()
            return

    Exec("ls -l", working_dir=".")
```

(NB: if you depend on a shell environment (e.g: Bundler or RVM), be sure to set `shell=True` when invoking Popen).

[dh](mailto:david.hodges@lonelyplanet.com.au).

---

References:
* [Sublime API](http://www.sublimetext.com/docs/2/api_reference.html)
* [Plugin Guide](http://docs.sublimetext.info/en/latest/reference/plugins.html)
* [Plugin Tutorial](http://net.tutsplus.com/tutorials/python-tutorials/how-to-create-a-sublime-text-2-plugin/)

