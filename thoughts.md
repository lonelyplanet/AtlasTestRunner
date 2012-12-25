

## Thoughts on writing a Sublime Text 2 Plugin

* The Console is your friend: ``Ctrl-```. It's the best way to see what's going on, even though Sublime doesn't always log errors. Note that the Console is a Python prompt, so you can run commands interactively, and output Python's print() command from your code.

* If the plugin appears to have loaded but doesn't run, check your syntax (python source, object-literals and settings files). Syntax errors leave no trace if they break the plugin when loading.

* Sublime will try to re-load your plugin if any files change. This can help with small edits or the tweaking of settings files, but re-loading is unreliable and doesn't always show when something goes wrong. After any change, a quit and a restart is best, making sure to clear out any python bytecode files (*.pyc). 
As always, if you catch yourself repeating tasks, automate them:

```shell
    #!/bin/sh

    PLUGIN_DIR=`dirname $0`

    find $PLUGIN_DIR -iname \*.pyc | xargs rm

    subl -n $PLUGIN_DIR
    subl -n $HOME/projects/my/test/project
```

* Try to keep your plugin design de-coupled from Sublime. Even though plugins have to extend one of Sublime's Command classes, you can write a simple wrapper Command class that does little more than gather configuration settings. If these settings (including any needed Sublime callbacks) are passed as a config object to your plugin logic, then they can be mocked by tests, and your classes can run independently, giving access to the pydb command-line debugger. (NB: pydb won't work within a Sublime context).

* Any long-running code should be spun off in a separate thread to keep from blocking Sublime. The Default plugin has a comprehensive class (ExecCommand) to execute code asynchronously, though for a simpler alternative, simply pass a function to `thread.start_new_thread` :

```python
    from subprocess import Popen, PIPE
    from thread import start_new_thread

    class Exec(object):
      def __init__(self, cmd, working_dir, during=None, after=None):
        proc = Popen([cmd], cwd=working_dir, shell=True, stderr=PIPE)
        start_new_thread(self.handle_stderr, (proc.stderr,))

      def handle_stderr(self, stderr):
        while True:
          data = os.read(stderr.fileno(), 128*1024)
          if data != "":
            print(data)
          else:
            stderr.close()
            return
```

(NB: if you depend on any shell environment settings (such as Bundler or RVM), be sure to set `shell=True` when invoking Popen).

---

References:
* [Sublime API](http://www.sublimetext.com/docs/2/api_reference.html)
* [Plugin Guide](http://docs.sublimetext.info/en/latest/reference/plugins.html)
* [Plugin Tutorial](http://net.tutsplus.com/tutorials/python-tutorials/how-to-create-a-sublime-text-2-plugin/)

